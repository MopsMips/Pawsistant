import os
import sqlite3
import asyncio
import discord
from discord import app_commands, Interaction
from discord.ext import commands
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

DB_PATH = "birthdays.db"


# DB setup
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS birthdays (
            user_id INTEGER PRIMARY KEY,
            day INTEGER NOT NULL,
            month INTEGER NOT NULL
        );
    """
    )
    conn.commit()
    conn.close()


init_db()


class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.birthday_loop())

    def cog_unload(self):
        pass

    @app_commands.command(
        name="birthday",
        description="Verwalte deinen Geburtstag oder zeige die Liste an.",
    )
    @app_commands.describe(
        action="set/info/remove/list",
        day="Tag",
        month="Monat",
        user="Anderer Nutzer (optional)",
    )
    async def birthday(
        self,
        interaction: Interaction,
        action: str,
        day: int = None,
        month: int = None,
        user: discord.User = None,
    ):
        user_id = interaction.user.id

        if action == "set":
            if not day or not month or not (1 <= day <= 31) or not (1 <= month <= 12):
                await interaction.response.send_message(
                    "❌ Ungültiges Datum.", ephemeral=True
                )
                return
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(
                "REPLACE INTO birthdays (user_id, day, month) VALUES (?, ?, ?)",
                (user_id, day, month),
            )
            conn.commit()
            conn.close()
            await interaction.response.send_message(
                f"🎂 Geburtstag gespeichert: {day:02d}.{month:02d}", ephemeral=True
            )

        elif action == "info":
            target = user or interaction.user
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(
                "SELECT day, month FROM birthdays WHERE user_id = ?", (target.id,)
            )
            row = c.fetchone()
            conn.close()
            if row:
                await interaction.response.send_message(
                    f"📅 {target.display_name} hat am {row[0]:02d}.{row[1]:02d} Geburtstag.",
                    ephemeral=not user,
                )
            else:
                await interaction.response.send_message(
                    "❌ Kein Geburtstag gefunden.", ephemeral=True
                )

        elif action == "remove":
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("DELETE FROM birthdays WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
            await interaction.response.send_message(
                "🗑️ Geburtstagseintrag gelöscht.", ephemeral=True
            )

        elif action == "list":
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT user_id, day, month FROM birthdays ORDER BY month, day")
            rows = c.fetchall()
            conn.close()

            if not rows:
                await interaction.response.send_message(
                    "📭 Noch keine Geburtstage gespeichert.", ephemeral=True
                )
                return

            lines = []
            for uid, day, month in rows:
                member = interaction.guild.get_member(uid)
                name = member.display_name if member else f"<@{uid}>"
                lines.append(f"{day:02d}.{month:02d} – {name}")

            message = "📅 **Geburtstagsliste:**\n" + "\n".join(lines)
            await interaction.response.send_message(message)

        else:
            await interaction.response.send_message(
                "❌ Ungültige Aktion. Verfügbare Optionen: set, info, remove, list",
                ephemeral=True,
            )

    @app_commands.command(
        name="birthday_check_now",
        description="(Admin) Führe den Geburtstagscheck manuell aus.",
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.default_permissions(manage_messages=True)
    async def birthday_check_now(self, interaction: Interaction):
        await interaction.response.send_message(
            "🔄 Geburtstags-Check wird ausgeführt...", ephemeral=True
        )
        await self.check_birthdays()

    async def birthday_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            now = datetime.now(ZoneInfo("Europe/Berlin"))
            next_run = now.replace(hour=7, minute=0, second=0, microsecond=0)
            if now >= next_run:
                next_run += timedelta(days=1)
            wait_seconds = (next_run - now).total_seconds()
            print(
                f"[Birthday] Warte bis {next_run.strftime('%Y-%m-%d %H:%M:%S')} für nächsten Check"
            )
            await asyncio.sleep(wait_seconds)
            await self.check_birthdays()

    async def check_birthdays(self):
        now = datetime.now(ZoneInfo("Europe/Berlin"))
        print(f"[Birthday] Führe Geburtstagsprüfung aus für {now.strftime('%d.%m.%Y')}")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            "SELECT user_id FROM birthdays WHERE day = ? AND month = ?",
            (now.day, now.month),
        )
        birthday_ids = [row[0] for row in c.fetchall()]
        conn.close()

        if not birthday_ids:
            print("[Birthday] Keine Geburtstage heute.")
            return

        channel_ids = os.getenv("DISCORD_BIRTHDAY_CHANNEL_ID", "").split("/")
        role_name = "Happy Birthday 🎉"

        for guild in self.bot.guilds:
            role = discord.utils.get(guild.roles, name=role_name)
            for uid in birthday_ids:
                member = guild.get_member(uid)
                if member:
                    for cid in channel_ids:
                        channel = guild.get_channel(int(cid))
                        if channel:
                            await channel.send(
                                f"🎉 Happy Birthday, {member.mention}! 🎂"
                            )
                            print(
                                f"[Birthday] Nachricht gesendet an {channel.name} für {member.display_name}"
                            )
                    if role:
                        await member.add_roles(role)
                        print(f"[Birthday] Rolle vergeben an {member.display_name}")

                        async def remove_role_later(m):
                            await asyncio.sleep(86400)
                            await m.remove_roles(role)
                            print(f"[Birthday] Rolle entfernt von {m.display_name}")

                        self.bot.loop.create_task(remove_role_later(member))


async def setup(bot):
    await bot.add_cog(Birthday(bot))

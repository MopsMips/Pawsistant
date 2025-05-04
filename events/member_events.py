import os
import random
import discord
from discord.ext import commands
from utils.tenor import get_tenor_gif

# Welcome messages for new members joining the server
welcome_messages = [
    "Look who's here! It's {member} – everyone act normal. 😎",
    "Welcome to the party, {member}! 🎉",
    "Brace yourselves... {member} just landed. 💥",
    "Welcome, {member}! You’re just in time for the chaos. 🎉",
    "We’ve been expecting you, {member}. ☕",
    "Alert 🚨: Awesome human detected – welcome, {member}!",
    "{member} just joined. Say hi or feel the guilt. 👀",
    "Hey {member}, your adventure starts here! ✨",
    "It’s dangerous to go alone, take this... and welcome {member}! 🗡️",
    "Welcome, {member}! You’re now part of the coolest crew. 😎",
]


def setup(bot: commands.Bot):
    @bot.event
    async def on_member_join(member: discord.Member):
        # Role assignment when joining
        role_ids = os.getenv("DISCORD_AUTO_ROLE_IDS", "").split("/")
        for role_id in role_ids:
            try:
                role = member.guild.get_role(int(role_id.strip()))
                if role:
                    await member.add_roles(role)
                    print(f"✅ Rolle '{role.name}' an {member.display_name} vergeben.")
                else:
                    print(f"⚠️ Rolle mit ID {role_id.strip()} nicht gefunden.")
            except ValueError:
                print(f"❌ Ungültige Rollen-ID: {role_id}")

        # Welcome message and GIF
        env_ids = os.getenv("DISCORD_WELCOME_CHANNEL_IDS", "")
        WELCOME_CHANNEL_IDS = [
            int(cid.strip()) for cid in env_ids.split("/") if cid.strip()
        ]
        for channel_id in WELCOME_CHANNEL_IDS:
            channel = member.guild.get_channel(channel_id)
            if channel:
                message = random.choice(welcome_messages).format(member=member.mention)
                gif_url = await get_tenor_gif("hello there")  # "welcome" or "hello"

                await channel.send(message)
                print(f"✅ Willkommensnachricht gesendet an #{channel.name}: {message}")

                if gif_url:
                    await channel.send(gif_url)
                    print(f"🖼️ GIF gesendet: {gif_url}")
                else:
                    print(f"⚠️ Kein GIF gefunden.")
            else:
                print(f"❌ Channel mit ID {channel_id} nicht gefunden.")

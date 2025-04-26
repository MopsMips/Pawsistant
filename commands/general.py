import random
import asyncio
from discord import app_commands, Interaction
from discord.ext import commands


# Check if user is allowed to manage messages
async def has_manage_messages_permission(interaction: Interaction) -> bool:
    return interaction.user.guild_permissions.manage_messages


def setup(tree: app_commands.CommandTree, bot: commands.Bot):

    #  Global error handler for all slash commands
    @tree.error
    async def on_app_command_error(interaction: Interaction, error):
        if isinstance(error, app_commands.errors.CheckFailure):
            await interaction.response.send_message(
                "❌ Du hast keine Berechtigung, diesen Befehl zu nutzen.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "❌ Ein unerwarteter Fehler ist aufgetreten.", ephemeral=True
            )
        raise error

    # Ping Command
    @tree.command(name="ping", description="Zeigt die Latenz des Bots an.")
    async def ping(interaction: Interaction):
        latency = round(bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! Latenz: {latency}ms")

    # Roll Command
    @tree.command(
        name="roll",
        description="Würfelt eine Zahl zwischen 1 und einem Maximalwert (Standard: 100).",
    )
    @app_commands.describe(max="Die höchste mögliche Zahl (Standard: 100)")
    async def roll(interaction: Interaction, max: int = 100):
        if max < 1:
            await interaction.response.send_message(
                "❌ Bitte gib eine gültige Zahl größer als 0 an.", ephemeral=True
            )
            return
        number = random.randint(1, max)
        await interaction.response.send_message(
            f"🎲 {interaction.user.display_name} würfelt eine {number} (1–{max})!"
        )

    # Clear Command (Admins only)
    @tree.command(
        name="clear",
        description="Löscht eine bestimmte Anzahl an Nachrichten. (Nur Admins)",
    )
    @app_commands.describe(amount="Anzahl der zu löschenden Nachrichten")
    @app_commands.check(has_manage_messages_permission)
    @app_commands.default_permissions(manage_messages=True)
    async def clear(interaction: Interaction, amount: int):
        if amount < 1:
            await interaction.response.send_message(
                "❌ Bitte gib eine gültige Anzahl (> 0) an.", ephemeral=True
            )
            return

        await interaction.response.defer(ephemeral=True)

        deleted = await interaction.channel.purge(limit=amount)

        confirmation = await interaction.followup.send(
            f"🧹 {len(deleted)} Nachrichten wurden gelöscht."
        )

        await asyncio.sleep(5)
        await confirmation.delete()

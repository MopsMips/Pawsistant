import random
from discord import app_commands, Interaction
from discord.ext import commands


# Check if user has permission to manage messages
async def has_manage_messages_permission(interaction: Interaction) -> bool:
    return interaction.user.guild_permissions.manage_messages


def setup(tree: app_commands.CommandTree, bot: commands.Bot):

    # Ping Command
    @tree.command(name="ping", description="Zeigt die Latenz des Bots an.")
    async def ping(interaction: Interaction):
        latency = round(bot.latency * 1000)
        await interaction.response.send_message(f"🏓 Pong! Latenz: {latency}ms")

    # Dice Roll Command
    @tree.command(
        name="roll",
        description="Würfelt eine Zahl zwischen 1 und einem Maximalwert (Standard: 100).",
    )
    @app_commands.describe(max="Die höchste mögliche Zahl (Standard: 100)")
    async def roll(interaction: Interaction, max: int = 100):
        if max < 1:
            await interaction.response.send_message(
                "❌ Die maximale Zahl muss größer als 0 sein.", ephemeral=True
            )
            return
        number = random.randint(1, max)
        await interaction.response.send_message(
            f"🎲 {interaction.user.display_name} würfelt eine {number} (1–{max})!"
        )

    # Clear Command (Admins)
    @tree.command(
        name="clear",
        description="Löscht eine bestimmte Anzahl an Nachrichten. (Nur Admins)",
    )
    @app_commands.describe(amount="Anzahl der zu löschenden Nachrichten")
    @app_commands.check(has_manage_messages_permission)
    async def clear(interaction: Interaction, amount: int):
        if amount < 1:
            await interaction.response.send_message(
                "❌ Bitte gib eine gültige Anzahl (> 0) an.", ephemeral=True
            )
            return

        deleted = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(
            f"🧹 {len(deleted)} Nachrichten wurden gelöscht.", ephemeral=True
        )

    # Error handling for missing authorizations
    @clear.error
    async def clear_error(interaction: Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                "❌ Du hast keine Berechtigung, diesen Befehl zu nutzen.",
                ephemeral=True,
            )
        else:
            raise error

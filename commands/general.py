import random
from discord import app_commands, Interaction


def setup(tree, bot):

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
                "❌ Die maximale Zahl muss größer als 0 sein."
            )
            return
        number = random.randint(1, max)
        await interaction.response.send_message(
            f"🎲 {interaction.user.display_name} würfelt eine {number} (1–{max})!"
        )

import os
import discord
from discord.ext import commands
from discord import app_commands, Interaction
import asyncio
import aiohttp
import random
from dotenv import load_dotenv

load_dotenv()

# Intents setzen
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.message_content = True

# Bot erstellen
bot = commands.Bot(command_prefix="/", intents=intents)

# Multible Channel IDs
ALLOWED_CHANNEL_IDS = os.getenv("DISCORD_CREATE_CHANNEL_ID", "").split("/")


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ PawBot ist online als {bot.user}")


# Slash Commands


# Bot-Info Latenz
@bot.tree.command(name="ping", description="Zeigt die Latenz des Bots an.")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! Latenz: {latency}ms")


# Würfelt eine Zahl zwischen 1 und einem Maximalwert (Standard: 100)
@bot.tree.command(
    name="roll",
    description="Würfelt eine Zahl zwischen 1 und einem Maximalwert (Standard: 100).",
)
@app_commands.describe(max="Die höchste mögliche Zahl (Standard: 100)")
async def roll(interaction: discord.Interaction, max: int = 100):
    if max < 1:
        await interaction.response.send_message(
            "❌ Die maximale Zahl muss größer als 0 sein."
        )
        return
    number = random.randint(1, max)
    await interaction.response.send_message(
        f"🎲 {interaction.user.display_name} würfelt eine {number} (1–{max})!"
    )


# Voice-Channel Automatik
@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and str(after.channel.id) in ALLOWED_CHANNEL_IDS:
        guild = after.channel.guild
        category = after.channel.category

        temp_channel = await guild.create_voice_channel(
            name=f"{member.display_name}'s Channel", category=category
        )

        await member.move_to(temp_channel)

        while True:
            await asyncio.sleep(2)
            if len(temp_channel.members) == 0:
                await temp_channel.delete()
                break


# Message-Events


# Massage-Event für GIFs bei "🔥"
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "🔥" in message.content:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://g.tenor.com/v1/search?q=firefighter&key=LIVDSRZULELA&limit=10"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    gifs = data.get("results")
                    if gifs:
                        try:
                            gif_url = random.choice(gifs)["media"][0]["gif"]["url"]
                            await message.channel.send(gif_url)
                        except (KeyError, IndexError):
                            await message.channel.send(
                                "🚒 Uuups! Konnte kein GIF laden."
                            )

    await bot.process_commands(message)


# Bot starten
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

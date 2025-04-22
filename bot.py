import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

load_dotenv()

# Intents setzen
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.message_content = True  # optional, falls du später Nachrichten-Befehle hinzufügen willst

# Bot erstellen
bot = commands.Bot(command_prefix="!", intents=intents)

# Liste von erlaubten Channel-IDs laden (getrennt durch '/')
ALLOWED_CHANNEL_IDS = os.getenv("DISCORD_CREATE_CHANNEL_ID", "").split("/")

@bot.event
async def on_ready():
    print(f"✅ PawBot ist online als {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    # Nur ausführen, wenn der Benutzer in einen Channel kommt
     if after.channel and str(after.channel.id) in ALLOWED_CHANNEL_IDS:
        guild = after.channel.guild
        category = after.channel.category

        # Temporären Channel erstellen
        temp_channel = await guild.create_voice_channel(
            name=f"{member.display_name}'s Channel",
            category=category
        )

        # Nutzer in neuen Channel verschieben
        await member.move_to(temp_channel)

        # Channel überwachen und löschen, wenn leer
        while True:
            await asyncio.sleep(2)
            if len(temp_channel.members) == 0:
                await temp_channel.delete()
                break

# Bot starten 
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
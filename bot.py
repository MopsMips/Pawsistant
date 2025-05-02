import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Modules
from commands import general
from events import message_events, reaction_events, voice_events, member_events

# Load .env file
load_dotenv()

# Intents setup
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.message_content = True

# Bot Setup
bot = commands.Bot(command_prefix="/", intents=intents)


# Bot Events
@bot.event
async def on_ready():
    general.setup(bot.tree, bot)  # Slash Commands
    message_events.setup(bot)  # Message Events
    reaction_events.setup(bot)  # Reaction Events
    voice_events.setup(bot)  # Voice Channel Auto Creation
    member_events.setup(bot)  # Member Welcome Messages

    # Load all cogs
    await bot.load_extension("commands.birthday")

    await bot.tree.sync()
    print(f"✅ PawBot ist online als {bot.user}")


# Bot launch
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

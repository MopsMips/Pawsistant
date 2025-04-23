import os
import discord
from discord.ext import commands
from discord import app_commands, Interaction
import asyncio
import aiohttp
import random
from dotenv import load_dotenv

load_dotenv()

# Intents setup
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True
intents.message_content = True

# Bot setup
bot = commands.Bot(command_prefix="/", intents=intents)

# Multible Channel IDs
ALLOWED_CHANNEL_IDS = os.getenv("DISCORD_CREATE_CHANNEL_ID", "").split("/")

# Message ID for Reaction roles
reaction_message_id = int(os.getenv("DISCORD_RULES_MESSAGE_ID"))

reaction_roles = {
    "✅": "Verified",  # Emoji : Rollenname
}


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ PawBot ist online als {bot.user}")


# Slash Commands
@bot.tree.command(name="ping", description="Zeigt die Latenz des Bots an.")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! Latenz: {latency}ms")


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


# Reaction roles with support for multiple message IDs from the .env file

# Rules-Message ID
reaction_message_ids = [
    int(message_id) for message_id in os.getenv("DISCORD_RULES_MESSAGE_ID").split("/")
]
# Reaction
reaction_roles = {
    "✅": "Verified",  # Emoji : Rolename
}


# Rules accepted - role added
@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id not in reaction_message_ids:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    role_name = reaction_roles.get(str(payload.emoji))
    if role_name:
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            member = guild.get_member(payload.user_id)
            if member and role not in member.roles:
                await member.add_roles(role)
                print(f"✅ Rolle {role_name} zu {member.display_name} hinzugefügt.")


# Rules rejected - role removed
@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id not in reaction_message_ids:
        return

    guild = bot.get_guild(payload.guild_id)
    if guild is None:
        return

    role_name = reaction_roles.get(str(payload.emoji))
    if role_name:
        role = discord.utils.get(guild.roles, name=role_name)
        if role:
            member = guild.get_member(payload.user_id)
            if member and role in member.roles:
                await member.remove_roles(role)
                print(f"❌ Rolle {role_name} von {member.display_name} entfernt.")


# Voice channel automatic


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


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Crazy-Meme
    if "crazy" in message.content.lower():
        meme_text = (
            "Crazy? I was crazy once. They locked me in a room. "
            "A rubber room. A rubber room with rats. "
            "And rats make me crazy..."
        )

        embed = discord.Embed(description=meme_text)
        embed.set_image(url="https://i.imgur.com/ZUN7Ko0.jpg")
        await message.channel.send(embed=embed)

    # Firefighter GIFs
    if "🔥" in message.content:
        api_key = os.getenv("TENOR_API_KEY", "LIVDSRZULELA")

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://tenor.googleapis.com/v2/search?q=firefighter&key={api_key}&limit=50&random=true"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    gifs = data.get("results")
                    if gifs:
                        try:
                            gif = random.choice(gifs)
                            gif_url = gif["media_formats"]["gif"]["url"]
                            await message.channel.send(gif_url)
                        except (KeyError, IndexError):
                            await message.channel.send(
                                "🚒 Uuups! Konnte kein GIF laden."
                            )
                else:
                    await message.channel.send("🚒 Fehler beim Laden der GIFs.")

    await bot.process_commands(message)


# Bot run
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

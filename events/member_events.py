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
        # Channel-ID load from .env file
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

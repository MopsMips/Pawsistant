import asyncio
import os
import discord
from discord.ext import commands

ALLOWED_CHANNEL_IDS = []


def setup(bot: commands.Bot):
    global ALLOWED_CHANNEL_IDS
    ALLOWED_CHANNEL_IDS = os.getenv("DISCORD_CREATE_CHANNEL_ID", "").split("/")

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

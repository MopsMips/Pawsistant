import discord
from discord.ext import commands
from utils.tenor import get_random_firefighter_gif


def setup(bot: commands.Bot):
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
            gif_url = await get_random_firefighter_gif()
            if gif_url:
                await message.channel.send(gif_url)
            else:
                await message.channel.send("🚒 Fehler beim Laden des GIFs.")

        await bot.process_commands(message)

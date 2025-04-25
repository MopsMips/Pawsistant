import discord
from discord.ext import commands
from utils.tenor import get_tenor_gif


def setup(bot: commands.Bot):
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        print(f"📥 Message received from {message.author}: {message.content}")

        # Crazy-Meme
        if "crazy" in message.content.lower():
            print("😵 Crazy meme triggered!")
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
            print("🔥 Fire emoji recognized! - Try to load...")
            gif_url = await get_tenor_gif("firefighter")
            if gif_url:
                print("✅ GIF loaded successfully.")
                await message.channel.send(gif_url)
            else:
                print("❌ Error loading the GIF.")
                await message.channel.send("🚒 Error loading the GIF.")

        await bot.process_commands(message)

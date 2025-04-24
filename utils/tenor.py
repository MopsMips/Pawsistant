import aiohttp
import os
import random

# Firefighter GIFs from Tenor API


async def get_random_firefighter_gif():
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
                        return gif["media_formats"]["gif"]["url"]
                    except (KeyError, IndexError):
                        return None
            return None

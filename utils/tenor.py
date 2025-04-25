import aiohttp
import os
import random

# This module contains functions to fetch GIFs from the Tenor API.


async def get_tenor_gif(query: str):
    api_key = os.getenv("TENOR_API_KEY", "LIVDSRZULELA")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://tenor.googleapis.com/v2/search?q={query}&key={api_key}&limit=50&random=true"
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

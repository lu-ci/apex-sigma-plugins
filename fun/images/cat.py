import random
import aiohttp
import discord
from lxml import html


async def cat(cmd, message, args):
    cat_api_key = cmd.cfg['api_key']
    api_url = f'http://thecatapi.com/api/images/get?format=xml&results_per_page=100&api_key={cat_api_key}'
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as raw_page:
            results = html.fromstring(await raw_page.text())[0][0]
    choice = random.choice(results)
    image_url = str(choice[0].text)
    embed = discord.Embed(color=0xFFDC5D, title='🐱 Meow~')
    embed.set_image(url=image_url)
    await message.channel.send(None, embed=embed)

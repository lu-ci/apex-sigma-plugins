import secrets

import aiohttp
import discord
from lxml import html

cache = {}


async def gelbooru(cmd, message, args):
    global cache
    tags = '+'.join(args)
    if not tags:
        tags = 'nude'
    gelbooru_url = f'http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={tags}'
    if tags not in cache:
        async with aiohttp.ClientSession() as session:
            async with session.get(gelbooru_url) as data:
                data = await data.read()
                posts = html.fromstring(data)
                cache.update({tags: posts})
    collection = cache.get(tags)
    if collection:
        choice = collection.pop(secrets.randbelow(len(collection)))
        img_url = choice.attrib['file_url']
        if not img_url.startswith('http'):
            img_url = f"https:{choice.attrib['file_url']}"
        post_url = f'https://gelbooru.com/index.php?page=post&s=view&id={choice.attrib["id"]}'
        icon_url = 'https://gelbooru.com/favicon.png'
        response = discord.Embed(color=0x006ffa)
        response.set_author(name='Gelbooru', icon_url=icon_url, url=post_url)
        footer_text = f'Score: {choice.attrib["score"]} | Size: {choice.attrib["width"]}x{choice.attrib["height"]}'
        response.set_image(url=img_url)
        response.set_footer(text=footer_text)
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 Search yielded no results.')
    await message.channel.send(None, embed=response)

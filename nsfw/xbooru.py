import aiohttp
import discord
import secrets
from lxml import html


async def xbooru(cmd, message, args):
    tags = '+'.join(args)
    try:
        if tags == '':
            tags = 'nude'
        gelbooru_url = 'http://xbooru.com/index.php?page=dapi&s=post&q=index&tags=' + tags
        async with aiohttp.ClientSession() as session:
            async with session.get(gelbooru_url) as data:
                data = await data.read()
        posts = html.fromstring(data)
        choice = secrets.choice(posts)
        img_url = choice.attrib['file_url']
        if not img_url.startswith('http'):
            img_url = f"http:{choice.attrib['file_url']}"
        post_url = f'http://xbooru.com/index.php?page=post&s=view&id={choice.attrib["id"]}'
        icon_url = 'http://xbooru.com/apple-touch-icon-152x152-precomposed.png'
        embed = discord.Embed(color=0xfede80)
        embed.set_author(name='Xbooru', icon_url=icon_url, url=post_url)
        embed.set_image(url=img_url)
        embed.set_footer(
            text=f'Score: {choice.attrib["score"]} | Size: {choice.attrib["width"]}x{choice.attrib["height"]}')
        await message.channel.send(None, embed=embed)
    except Exception:
        embed = discord.Embed(color=0x696969, title=f'🔍 Search for {tags} yielded no results.')
        await message.channel.send(None, embed=embed)

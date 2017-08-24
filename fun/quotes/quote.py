import json
import aiohttp
import discord


async def quote(cmd, message, args):
    resource = 'http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en'
    data = None
    while not data:
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as data:
                data = await data.read()
                data = json.loads(data)
    text = data['quoteText']
    while text.endswith(' '):
        text = text[:-1]
    if 'quoteAuthor' in data:
        author = data['quoteAuthor']
    else:
        author = 'Unknown'
    if not author:
        author = 'Unknown'
    quote_text = f'\"{text}\"\n'
    embed = discord.Embed(color=0xF9F9F9)
    embed.add_field(name=f'📑 A Quote From {author}', value=quote_text)
    await message.channel.send(None, embed=embed)

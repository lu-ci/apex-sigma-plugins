import aiohttp
import discord
from lxml import html as l


async def visualnovelquote(cmd, message, args):
    source_page = 'https://vndb.org/r'
    vndb_icon = 'https://i.imgur.com/YrK5tQF.png'
    async with aiohttp.ClientSession() as session:
        async with session.get(source_page) as data:
            data = await data.text()
    page = l.fromstring(data)
    footer_quote = page.cssselect('#footer a')[0]
    quote_text = footer_quote.text_content().strip()
    quote_url = f"https://vndb.org{footer_quote.attrib['href']}"
    async with aiohttp.ClientSession() as session:
        async with session.get(quote_url) as quote_page:
            quote_page = await quote_page.text()
    quote_page = l.fromstring(quote_page)
    vn_title = quote_page.cssselect('.stripe')[0][0][1].text_content().strip()
    vn_image = quote_page.cssselect('.vnimg')[0][0][0].attrib['src']
    response = discord.Embed(color=0x225588)
    response.set_author(name=vn_title, url=quote_url, icon_url=vndb_icon)
    response.description = quote_text
    response.set_thumbnail(url=vn_image)
    await message.channel.send(embed=response)

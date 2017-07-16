import discord
from sigma.core.utilities.data_processing import user_avatar


async def avatar(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    ava_url = user_avatar(target)
    embed = discord.Embed(color=target.color)
    embed.set_image(url=ava_url)
    await message.channel.send(None, embed=embed)

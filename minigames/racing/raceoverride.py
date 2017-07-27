import discord
from .nodes.race_storage import *


async def raceoverride(cmd, message, args):
    if message.channel.id in races:
        del races[message.channel.id]
        response = discord.Embed(color=0xFF9900, title='🔥 Race obliderated.')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ No race in this channel.')
    await message.channel.send(embed=response)

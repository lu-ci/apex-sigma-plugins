import discord

from sigma.plugins.interactions.mech.response_grabber import grab_response
from sigma.plugins.interactions.mech.targetting import get_target


async def cuddle(cmd, message, args):
    resp = grab_response(cmd.resource('responses.yml'), 'cuddle')
    target = get_target(message, args)
    if not target or target.id == message.author.id:
        response = discord.Embed(color=0xffcc4d, title=f'☺ {message.author.name} tries to cuddle with themself.')
    else:
        response = discord.Embed(color=0xffcc4d, title=f'☺ {message.author.name} cuddles with {target.name}.')
    response.set_image(url=resp['url'])
    response.set_footer(text=f'Submitted by {resp["auth"]} from {resp["srv"]}.')
    await message.channel.send(embed=response)

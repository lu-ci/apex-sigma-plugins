import discord
from sigma.plugins.interactions.mech.response_grabber import grab_response
from sigma.plugins.interactions.mech.targetting import get_target, make_footer


async def stare(cmd, message, args):
    resp = grab_response(cmd.resource('responses.yml'), 'stare')
    target = get_target(message, args)
    if not target or target.id == message.author.id:
        response = discord.Embed(color=0xF9F9F9, title=f'👀 {message.author.name} stares.')
    else:
        response = discord.Embed(color=0xF9F9F9, title=f'👀 {message.author.name} stares at {target.name}.')
    response.set_image(url=resp['url'])
    response.set_footer(text=make_footer(cmd, resp))
    await message.channel.send(embed=response)

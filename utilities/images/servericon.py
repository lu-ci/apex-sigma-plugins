import discord


async def servericon(cmd, message, args):
    embed = discord.Embed(color=0x0099FF)
    embed.set_image(url=message.guild.icon_url)
    await message.channel.send(None, embed=embed)

import discord


async def repeat(cmd, message, args):
    if message.guild.id in cmd.bot.music.repeaters:
        cmd.bot.music.repeaters.remove(message.guild.id)
        response = discord.Embed(color=0x0099FF, title='🔁 Queue Repeat Disabled')
    else:
        cmd.bot.music.repeaters.append(message.guild.id)
        response = discord.Embed(color=0x0099FF, title='🔁 Queue Repeat Enabled')
    await message.channel.send(None, embed=response)

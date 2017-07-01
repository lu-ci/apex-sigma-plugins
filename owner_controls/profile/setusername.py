import discord


async def setusername(cmd, message, args):
    name_input = ' '.join(args)
    try:
        await cmd.bot.user.edit(username=name_input)
        response = discord.Embed(color=0x66CC66, title=f'✅ Changed username to {name_input}.')
    except:
        response = discord.Embed(color=0xDB0000, title=f'❗ I was unable to change my username.')
    await message.channel.send(embed=response)

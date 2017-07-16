import secrets
import discord


async def roll(cmd, message, args):
    if args:
        try:
            endrange = int(args[0])
        except ValueError:
            embed = discord.Embed(color=0xDB0000, title='❗ Only integers are accepted.')
            await message.channel.send(None, embed=embed)
            return
    else:
        endrange = 100
    number = secrets.randbelow(endrange) + 1
    num = str(number)
    if len(num) > 1950:
        num = num[:1950] + '...'
    embed = discord.Embed(color=0xea596e)
    embed.add_field(name='🎲 You Rolled', value=num)
    await message.channel.send(None, embed=embed)

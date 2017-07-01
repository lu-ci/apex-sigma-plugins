import discord
import inspect


async def evaluatecode(cmd, message, args):
    if not args:
        status = discord.Embed(color=0xDB0000, title='❗ Nothing Inputted To Process')
    else:
        try:
            execution = " ".join(args)
            output = eval(execution)
            if inspect.isawaitable(output):
                output = await output
            status = discord.Embed(title='✅ Executed', color=0x66CC66)
            status.add_field(name='Results', value=f'\n```\n{output}\n```')
        except Exception as e:
            status = discord.Embed(color=0xDB0000, title='❗ Error')
            status.add_field(name='Execution Failed', value=f'{e}')
    await message.channel.send(None, embed=status)

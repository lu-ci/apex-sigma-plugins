async def test(cmd, message, args):
    await message.channel.send(f'Latency: {cmd.bot.latency}')

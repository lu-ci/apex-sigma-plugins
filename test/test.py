async def sigma_command(cmd, message, args):
    await message.channel.send(' '.join(args))
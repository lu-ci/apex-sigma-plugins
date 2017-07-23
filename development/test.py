async def test(cmd, message, args):
    url = ''.join(args)
    info = await cmd.bot.music.extract_info(url)
    print(info)

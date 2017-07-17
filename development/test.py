async def test(cmd, message, args):
    if not message.guild.me.voice:
        await message.author.voice.channel.connect()
    url = 'https://www.youtube.com/watch?v=XiqYyoARr5g&feature=youtu.be'
    item = {'url': url}
    await cmd.bot.music.play(message.guild, item)
    await message.channel.send('Ok.')

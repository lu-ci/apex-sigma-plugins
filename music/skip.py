async def skip(cmd, message, args):
    if message.author.voice:
        if message.author.voice.channel.id == message.guild.me.voice.channel.id:
            message.guild.voice_client.stop()

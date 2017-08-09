async def musicoverride(cmd, message, args):
    if message.guild.voice_client:
        await message.guild.voice_client.disconnect()
    if message.author.voice:
        await message.author.voice.channel.connect()
    if message.guild.voice_client:
        await message.guild.voice_client.disconnect()

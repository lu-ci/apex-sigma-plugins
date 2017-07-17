import discord


async def stop(cmd, message, args):
    if message.guild.me.voice:
        await message.guild.voice_client.disconnect()
        response = discord.Embed(color=0x66CC66, title=f'✅ Disconnected From {message.guild.me.voice.channel.name}.')
        await message.channel.send(embed=response)

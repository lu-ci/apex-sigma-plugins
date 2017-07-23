import discord


async def summon(cmd, message, args):
    if message.author.voice:
        if message.guild.voice_client:
            if message.author.voice.channel.id != message.guild.voice_client.channel.id:
                await message.guild.voice_client.move_to(message.author.voice.channel)
                title = f'🚩 Moved to {message.author.voice.channel.name}.'
                response = discord.Embed(color=0xdd2e44, title=title)
            else:
                response = discord.Embed(color=0xDB0000, title='❗ We are in the same channel.')
        else:
            await message.author.voice.channel.connect()
            title = f'🚩 Connected to {message.author.voice.channel.name}.'
            response = discord.Embed(color=0xdd2e44, title=title)
    else:
        response = discord.Embed(color=0xDB0000, title='❗ You are not in a voice channel.')
    await message.channel.send(embed=response)

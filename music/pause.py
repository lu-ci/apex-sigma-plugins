import discord


async def pause(cmd, message, args):
    if message.author.voice:
        if message.guild.voice_client:
            if message.guild.voice_client.channel.id != message.author.voice.channel.id:
                same_bound = False
        if same_bound:
            if message.guild.voice_client:
                if message.guild.voice_client
            else:
                response = discord.Embed(color=0xBE1931, title='❗ I am not connected to a voice channel.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ You are not in my voice channel.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You are not in a voice channel.')
    await message.channel.send(embed=response)

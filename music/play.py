import discord
import asyncio
import datetime
from sigma.core.utilities.data_processing import user_avatar


async def play(cmd, message, args):
    if args:
        await cmd.bot.modules.commands['queue'].execute(message, args)
    queue = cmd.bot.music.get_queue(message.guild)
    voice = message.guild.me.voice
    if not voice or not message.guild.voice_client:
        author_voice = message.author.voice
        if author_voice:
            can_connect = message.guild.me.permissions_in(message.author.voice.channel).connect
            can_talk = message.guild.me.permissions_in(message.author.voice.channel).speak
            if can_connect and can_talk:
                await author_voice.channel.connect()
            else:
                title = f'❗ I am not allowed to join {message.author.voice.channel.name}.'
                embed = discord.Embed(title=title, color=0xDB0000)
                await message.channel.send(None, embed=embed)
                return
        else:
            response = discord.Embed(color=0xDB0000, title='❗ You are not in a voice channel.')
            await message.channel.send(embed=response)
            return
    if not queue.empty():
        if message.guild.voice_client and not message.guild.voice_client.is_playing():
            while not cmd.bot.music.get_queue(message.guild).empty():
                item = await cmd.bot.music.get_from_queue(message.guild)
                song_info = await cmd.bot.music.play(message.guild, item)
                embed = discord.Embed(color=0x0099FF)
                embed.add_field(name='🎵 Now Playing', value=song_info['title'])
                embed.set_thumbnail(url=song_info['thumbnail'])
                author_name = f'{item["requester"].name}#{item["requester"].discriminator}'
                embed.set_author(name=author_name, icon_url=user_avatar(item['requester']), url=item['url'])
                embed.set_footer(text=f'Duration: {str(datetime.timedelta(seconds=item["duration"]))}')
                await message.channel.send(embed=embed)
                while message.guild.voice_client.is_playing():
                    await asyncio.sleep(3)
            response = discord.Embed(color=0x0099FF, title='🎵 Queue done.')
        else:
            if not args:
                response = discord.Embed(title='❗ Already playing music.', color=0xDB0000)
            else:
                response = None
    else:
        response = discord.Embed(title='❗ The queue is empty.', color=0xDB0000)
    if response:
        await message.channel.send(embed=response)

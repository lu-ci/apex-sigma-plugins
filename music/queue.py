import asyncio
import discord
import datetime
from sigma.core.utilities.data_processing import search_youtube, user_avatar


async def queue(cmd, message, args):
    if args:
        qry = ' '.join(args)
        if qry.startswith('http'):
            url = qry
        else:
            url = await search_youtube(qry)
        if '?list=' not in url:
            info = await cmd.bot.music.get_song_info(url)
            data = {
                'requester': message.author,
                'url': url,
                'thumbnail': info['thumbnail'],
                'duration': info['duration'],
                'title': info['title']
            }
            await cmd.bot.music.add_to_queue(message.guild, data)
            author_name = f'{message.author.name}#{message.author.discriminator}'
            response = discord.Embed(color=0x66CC66)
            response.add_field(name='✅ Added To Queue', value=info['title'])
            response.set_thumbnail(url=info['thumbnail'])
            response.set_author(name=author_name, icon_url=user_avatar(message.author))
            response.set_footer(text=f'Duration: {str(datetime.timedelta(seconds=info["duration"]))}')
        else:
            response = discord.Embed(color=0xDB0000, title='❗ Playlist support not yet implemented.')
    else:
        response = None
        q = cmd.bot.music.get_queue(message.guild)
        q_bup = asyncio.Queue()
        if q.empty():
            embed = discord.Embed(color=0x0099FF, title='ℹ The Queue Is Empty')
            await message.channel.send(None, embed=embed)
        else:
            q_list = []
            while not q.empty():
                q_item = await q.get()
                q_list.append(q_item)
                await q_bup.put(q_item)
            q_list_mini = q_list[:5]
            cmd.bot.music.queues.update({message.guild.id: q_bup})
            embed = discord.Embed(color=0x0099FF,
                                  title=f'ℹ The {len(q_list_mini)} Upcoming Songs (Total: {len(q_list)})')
            for item in q_list_mini:
                duration = str(datetime.timedelta(seconds=item["duration"]))
                information = f'Requested By: {item["requester"].name}\nDuration: {duration}'
                embed.add_field(name=item['title'], value=f'```\n{information}\n```', inline=False)
            if message.guild.id in cmd.bot.music.repeaters:
                embed.set_footer(text='The current queue is set to repeat.')
            await message.channel.send(None, embed=embed)
    if response:
        await message.channel.send(embed=response)

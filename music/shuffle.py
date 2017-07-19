import discord
import secrets
import asyncio


async def shuffle(cmd, message, args):
    queue = cmd.bot.music.get_queue(message.guild.id)
    queue_new = asyncio.Queue()
    if queue:
        if not queue.empty():
            q_list = []
            while not cmd.bot.music.get_queue(message.guild.id).empty():
                q_item = await cmd.bot.music.get_queue(message.guild.id).get()
                q_list.append(q_item)
            new_list = []
            while len(q_list) != 0:
                picked_item = q_list.pop(secrets.randbelow(len(q_list)))
                new_list.append(picked_item)
            for item in new_list:
                await queue_new.put(item)
            cmd.bot.music.queues.update({message.guild.id: queue_new})
            embed = discord.Embed(color=0x0099FF, title='🔀 Queue Shuffled')
            await message.channel.send(None, embed=embed)

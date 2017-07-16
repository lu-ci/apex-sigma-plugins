import discord


async def channelinformation(cmd, message, args):
    if message.channel_mentions:
        chan = message.channel_mentions[0]
    else:
        chan = message.channel
    out_list = [
        ['Name', chan.name],
        ['Channel ID', chan.id],
        ['Created', chan.created_at],
        ['Is Default', chan.is_default()],
        ['Position', chan.position]
    ]
    if chan.topic:
        topic = chan.topic
    else:
        topic = 'None'
    out_list.append(['Topic', topic])
    embed = discord.Embed(title='#' + chan.name + ' Information', color=0x1ABC9C)
    for item in out_list:
        embed.add_field(name=str(item[0]), value=f'```python\n{item[1]}\n```')
    await message.channel.send(None, embed=embed)

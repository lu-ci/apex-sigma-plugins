import arrow
import discord


async def afk_mention_check(ev, message):
    if message.guild:
        if not message.content.startswith(ev.bot.get_prefix(message)):
            if message.mentions:
                target = message.mentions[0]
                afk_data = ev.db[ev.db.db_cfg.database]['AwayUsers'].find_one({'UserID': target.id})
                if afk_data:
                    time_then = arrow.get(afk_data['Timestamp'])
                    afk_time = arrow.get(time_then).humanize(arrow.utcnow()).title()
                    afk_reason = afk_data['reason']
                    if afk_reason.startswith('http'):
                        suffix = afk_reason.split('.')[-1]
                        if suffix in ['gif', 'jpg', 'jpeg', 'png']:
                            url = True
                        else:
                            url = False
                    else:
                        url = False
                    if url:
                        response = discord.Embed(color=0x3B88C3, title=f'ℹ {target.name} is AFK.',
                                                 timestamp=time_then.datetime)
                        response.set_thumbnail(url=afk_reason)
                    else:
                        response = discord.Embed(color=0x3B88C3, timestamp=time_then.datetime)
                        response.add_field(name=f'ℹ {target.name} is AFK.',
                                           value=f'Reason: {afk_data["Reason"]}\nWent AFK: {afk_time}')
                    await message.channel.send(embed=response)

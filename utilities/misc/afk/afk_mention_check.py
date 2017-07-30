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
                    response = discord.Embed(color=0x3B88C3, timestamp=time_then.datetime)
                    response.add_field(name=f'ℹ {target.name} is AFK.',
                                       value=f'Reason: {afk_data["Reason"]}\nWent AFK: {afk_time}')
                    await message.channel.send(embed=response)

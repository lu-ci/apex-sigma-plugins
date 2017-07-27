import discord
from sigma.core.utilities.data_processing import user_avatar

dan_id = 285232223127601152
dawn_id = 222234484064518156


async def dan_voice_track(ev, member, before, after):
    if member.id == dan_id:
        dbcol = ev.db[ev.db.db_cfg.database]['SpecialSettings']
        settings = dbcol.find_one({'Name': 'dan_tracker'})
        if settings is None:
            active = True
        else:
            active = settings['Value']
        if active:
            if after.channel:
                night = discord.utils.find(lambda x: x.id == dawn_id, ev.bot.get_all_members())
                if night:
                    response = discord.Embed(color=member.color)
                    title = f'{member.name} has joined {after.channel.name} on {member.guild.name}.'
                    response.set_author(name=title, icon_url=user_avatar(member))
                    await night.send(embed=response)

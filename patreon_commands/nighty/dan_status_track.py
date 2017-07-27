import discord
from sigma.core.utilities.data_processing import user_avatar

dan_id = 285232223127601152
dawn_id = 222234484064518156


async def dan_status_track(ev, before, after):
    if before.id == dan_id:
        dbcol = ev.db[ev.db.db_cfg.database]['SpecialSettings']
        settings = dbcol.find_one({'Name': 'dan_tracker'})
        if settings is None:
            active = True
        else:
            active = settings['Value']
        if active:
            if not ev.bot.cooldown.on_cooldown(ev.name, after):
                ev.bot.cooldown.set_cooldown(ev.name, after, 60)
                if before.status != after.status:
                    night = discord.utils.find(lambda x: x.id == dawn_id, ev.bot.get_all_members())
                    if night:
                        response = discord.Embed(color=after.color)
                        title = f'{after.name} is now {str(after.status).replace("dnd", "busy")}.'
                        response.set_author(name=title, icon_url=user_avatar(after))
                        await night.send(embed=response)

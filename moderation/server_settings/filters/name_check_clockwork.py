import asyncio
import discord
import string

async def name_check_clockwork(ev):
    ev.bot.loop.create_task(name_checker(ev))

async def name_checker(ev):
    while True:
        guild_ids = []
        guilds = []
        actives = ev.db[ev.db.db_cfg.database].ServerSettings.find({'ASCIIOnlyNames': True})
        for doc in actives:
            gid = doc['ServerID']
            guild_ids.append(gid)
        for guild_id in guild_ids:
            active_guild = discord.utils.find(lambda x: x.id == guild_id, ev.bot.guilds)
            if active_guild:
                guilds.append(active_guild)
        for guild in guilds:
            active = ev.db.get_guild_settings(guild.id, 'ASCIIOnlyNames')
            if active is None:
                active = False
            if active:
                temp_name = ev.db.get_guild_settings(guild.id, 'ASCIIOnlyTempName')
                if temp_name is None:
                    temp_name = '<ChangeMyName>'
                members = guild.members
                for member in members:
                    nam = member.display_name
                    invalid = False
                    for char in nam:
                        if char not in string.printable:
                            invalid = True
                            break
                    if invalid:
                        try:
                            await member.edit(nick=temp_name, reason='ASCII name enforcement.')
                        except discord.Forbidden:
                            pass
        await asyncio.sleep(60)

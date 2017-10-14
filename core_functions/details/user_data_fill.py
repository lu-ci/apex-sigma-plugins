import asyncio
from sigma.core.utilities.data_processing import user_avatar


async def user_data_fill(ev):
    ev.bot.loop.create_task(member_filler_loop(ev))


async def member_filler_loop(ev):
    while True:
        all_members = ev.bot.get_all_members()
        mem_coll = ev.db[ev.db.db_cfg.database].UserDetails
        mem_coll.drop()
        member_list = []
        for member in all_members:
            mem_data = {
                'Name': member.name,
                'Nickname': member.display_name,
                'Discriminator': member.discriminator,
                'UserID': member.id,
                'Avatar': user_avatar(member).split('?')[0],
                'Color': str(member.color)
            }
            member_list.append(mem_data)
        mem_coll.insert_many(member_list)
        await asyncio.sleep(3600)

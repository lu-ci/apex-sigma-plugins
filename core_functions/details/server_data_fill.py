import asyncio


async def server_data_fill(ev):
    ev.bot.loop.create_task(server_filler_loop(ev))


async def server_filler_loop(ev):
    while True:
        all_guilds = ev.bot.guilds
        srv_coll = ev.db[ev.db.db_cfg.database].ServerDetails
        srv_coll.drop()
        server_list = []
        for guild in all_guilds:
            srv_data = {
                'Name': guild.name,
                'ServerID': guild.id,
                'Icon': guild.icon_url or 'https://i.imgur.com/QnYSlld.png'
            }
            server_list.append(srv_data)
        srv_coll.insert_many(server_list)
        await asyncio.sleep(300)

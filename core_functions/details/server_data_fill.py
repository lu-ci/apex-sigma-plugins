import functools
from concurrent.futures import ThreadPoolExecutor

import arrow


async def server_data_fill(ev):
    ev.log.info('Filling server details...')
    threads = ThreadPoolExecutor(2)
    start_stamp = arrow.utcnow().float_timestamp
    srv_coll = ev.db[ev.db.db_cfg.database].ServerDetails
    srv_coll.drop()
    for x in range(0, ev.bot.shard_count):
        shard_start = arrow.utcnow().float_timestamp
        server_list = []
        for guild in ev.bot.guilds:
            if guild.shard_id == x:
                srv_data = {
                    'Name': guild.name,
                    'ServerID': guild.id,
                    'Icon': guild.icon_url or 'https://i.imgur.com/QnYSlld.png'
                }
                server_list.append(srv_data)
        task = functools.partial(srv_coll.insert, server_list)
        await ev.bot.loop.run_in_executor(threads, task)
        shard_end = arrow.utcnow().float_timestamp
        shard_diff = round(shard_end - shard_start, 3)
        ev.log.info(f'Filled Shard #{x} Servers in {shard_diff}s.')
    end_stamp = arrow.utcnow().float_timestamp
    diff = round(end_stamp - start_stamp, 3)
    ev.log.info(f'Server detail filler finished in {diff}s')

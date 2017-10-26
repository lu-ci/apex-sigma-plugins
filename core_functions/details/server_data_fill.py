import arrow
import functools
from concurrent.futures import ThreadPoolExecutor


async def server_data_fill(ev):
    ev.log.info('Filling server details...')
    threads = ThreadPoolExecutor(2)
    start_stamp = arrow.utcnow().float_timestamp
    ev.bot.cooldown.set_cooldown(ev.name, 'server_details', 3600)
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
    task = functools.partial(srv_coll.insert, server_list)
    await ev.bot.loop.run_in_executor(threads, task)
    end_stamp = arrow.utcnow().float_timestamp
    diff = round(end_stamp - start_stamp, 3)
    ev.log.info(f'Server detail filler finished in {diff}s')

import secrets
from sigma.core.utilities.stats_processing import add_special_stats

async def table_unflipper(ev, message):
    if '(╯°□°）╯︵ ┻━┻' in message.content:
        unflip = True
        if message.guild:
            flip_settings = ev.db.get_guild_settings(message.guild.id, 'Unflip')
            if flip_settings is None:
                unflip = False
            else:
                unflip = flip_settings
        if unflip:
            await add_special_stats(ev.db, 'tables_fixed')
            table = ['┬─┬ ノ( ^_^ノ)',
                     '┬─┬ ﾉ(° -°ﾉ)',
                     '┬─┬ ノ(゜-゜ノ)',
                     '┬─┬ ノ(ಠ\_ಠノ)',
                     '┻━┻~~~~  ╯(°□° ╯)',
                     '┻━┻====  ╯(°□° ╯)',
                     '┣ﾍ(^▽^ﾍ)Ξ(ﾟ▽ﾟ*)ﾉ┳━┳ There we go~♪',
                     ' ┬──┬﻿ ¯\_(ツ)',
                     '(ヘ･_･)ヘ┳━┳',
                     'ヘ(´° □°)ヘ┳━┳',
                     '┣ﾍ(≧∇≦ﾍ)… (≧∇≦)/┳━┳']
            await message.channel.send(secrets.choice(table))

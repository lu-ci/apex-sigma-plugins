from sigma.plugins.core_functions.chatterbot.nodes.cb_instance_storage import get_cb
from sigma.core.utilities.data_processing import user_avatar
from concurrent.futures import ThreadPoolExecutor
import functools
import asyncio
import discord

threads = ThreadPoolExecutor(max_workers=2)
loop = asyncio.get_event_loop()


async def cb_response(ev, message):
    db_cfg = ev.bot.cfg.db
    cb = get_cb(db_cfg)
    active = ev.db.get_guild_settings(message.guild.id, 'ChatterBot')
    if active:
        mention = f'<@{ev.bot.user.id}>'
        mention_alt = f'<@!{ev.bot.user.id}>'
        if message.content.startswith(mention) or message.content.startswith(mention_alt):
            args = message.content.split(' ')
            interaction = ' '.join(args[1:])
            if message.mentions:
                for mnt in message.mentions:
                    interaction = interaction.replace(mnt.mention, mnt.name)
            response = str(await loop.run_in_executor(threads, functools.partial(cb.get_response, interaction)))
            if not response.endswith(('.' or '?' or '!')):
                response += '.'
            resp_embed = discord.Embed(color=0x8ccaf7, title=f'🗨 {response}')
            resp_embed.set_author(name=message.author.display_name, icon_url=user_avatar(message.author))
            await message.channel.send(embed=resp_embed)

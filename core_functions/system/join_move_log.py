import discord
from .move_log_embed import make_move_log_embed
from sigma.core.utilities.data_processing import user_avatar


async def join_move_log(ev, guild):
    if ev.bot.cfg.pref.movelog_channel:
        mlc_id = ev.bot.cfg.pref.movelog_channel
        mlc = discord.utils.find(lambda x: x.id == mlc_id, ev.bot.get_all_channels())
        if mlc:
            log_embed = discord.Embed(color=0x66CC66)
            log_embed.set_author(name='Joined A Guild', icon_url=user_avatar(guild.owner))
            make_move_log_embed(log_embed, guild)
            await mlc.send(embed=log_embed)

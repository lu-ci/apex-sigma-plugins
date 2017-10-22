import discord
from sigma.core.utilities.server_bound_logging import log_event


async def avatar_logger(ev, before, after):
    guild = after.guild
    if guild:
        if before.avatar != after.avatar:
            log_edits = ev.db.get_guild_settings(guild.id, 'LogAvatars')
            if log_edits:
                log_embed = discord.Embed(color=0xF9F9F9)
                log_embed.set_author(name=f'User\'s Avatar Was Changed', icon_url=after.avatar_url)
                log_embed.add_field(name='Before', value=f'[Image Link]({before.avatar_url})')
                log_embed.add_field(name='After', value=f'[Image Link]({after.avatar_url})')
                log_embed.set_thumbnail(url=after.avatar_url)
                log_embed.set_footer(text='Old avatar is in the thumbnail. After is in the header.')
                await log_event(ev.db, guild, log_embed)

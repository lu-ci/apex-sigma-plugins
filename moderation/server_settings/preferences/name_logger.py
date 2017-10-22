import discord
from sigma.core.utilities.server_bound_logging import log_event


async def name_logger(ev, before, after):
    guild = after.guild
    if guild:
        if before.name != after.name:
            log_edits = ev.db.get_guild_settings(guild.id, 'LogNames')
            if log_edits:
                author = f'{after.author.name}#{after.discriminator}'
                log_embed = discord.Embed(color=0xF9F9F9)
                log_embed.set_author(name=f'{author} Edited Their Username', icon_url=after.avatar_url)
                log_embed.add_field(name='Before', value=f'{before.name}#{before.discriminator}')
                log_embed.add_field(name='After', value=f'{after.name}#{after.discriminator}')
                await log_event(ev.db, guild, log_embed)

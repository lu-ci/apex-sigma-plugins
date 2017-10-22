import discord
from sigma.core.utilities.server_bound_logging import log_event


async def nickname_logger(ev, before, after):
    guild = after.guild
    if guild:
        if before.display_name != after.display_name:
            if not (after.name != after.display_name and before.name != before.display_name):
                log_edits = ev.db.get_guild_settings(guild.id, 'LogNicknames')
                if log_edits:
                    author = f'{after.name}#{after.discriminator}'
                    log_embed = discord.Embed(color=0xF9F9F9)
                    log_embed.set_author(name=f'{author} Edited Their Nickname', icon_url=after.avatar_url)
                    log_embed.add_field(name='Before', value=before.display_name)
                    log_embed.add_field(name='After', value=after.display_name)
                    await log_event(ev.db, guild, log_embed)

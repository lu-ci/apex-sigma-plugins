import discord
from sigma.core.utilities.server_bound_logging import log_event


async def edit_logger(ev, before, after):
    guild = after.guild
    if guild:
        if len(after.content) <= 550:
            log_edits = ev.db.get_guild_settings(guild.id, 'LogMessageEdits')
            if log_edits:
                author = f'{after.author.name}#{after.author.discriminator}'
                log_embed = discord.Embed(color=0xF9F9F9)
                log_embed.set_author(name=f'{author} Edited Their Message', icon_url=after.author.avatar_url)
                log_embed.add_field(name='Before', value=before.content, inline=False)
                log_embed.add_field(name='After', value=after.content, inline=False)
                log_embed.set_footer(text=f'Edited in #{after.channel.name}.')
                await log_event(ev.db, guild, log_embed)

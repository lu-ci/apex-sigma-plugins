import discord
from sigma.core.utilities.server_bound_logging import log_event


async def delete_logger(ev, message):
    if message.guild:
        if len(message.content) <= 800:
            log_edits = ev.db.get_guild_settings(message.guild.id, 'LogMessageDeletes')
            if log_edits:
                author = f'{message.author.name}#{message.author.discriminator}'
                log_embed = discord.Embed(color=0xF9F9F9)
                log_embed.set_author(name=f'{author}\'s Message Was Deleted', icon_url=message.author.avatar_url)
                log_embed.add_field(name='Content', value=message.content, inline=False)
                log_embed.set_footer(text=f'Deleted from #{message.channel.name}.')
                await log_event(ev.db, message.guild, log_embed)

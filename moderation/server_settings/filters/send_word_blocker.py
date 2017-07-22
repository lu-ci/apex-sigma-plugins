import discord
from .cleaners import clean_content


async def send_word_blocker(ev, message):
    if message.guild:
        text = clean_content(message.content.lower())
        elements = text.split(' ')
        blocked_words = ev.db.get_guild_settings(message.guild.id, 'BlockedWords')
        if blocked_words is None:
            blocked_words = []
        remove = False
        reason = None
        for word in blocked_words:
            if word in elements:
                remove = True
                reason = word
                break
        if remove:
            try:
                await message.delete(reason=f'Contains a blocked word: "{reason}".')
                title = f'🔥 Your message was deleted for containing "{reason}".'
                to_author = discord.Embed(color=0xFF9900, title=title)
                try:
                    await message.author.send(embed=to_author)
                except discord.ClientException:
                    pass
            except discord.ClientException:
                pass

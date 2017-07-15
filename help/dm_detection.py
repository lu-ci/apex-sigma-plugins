import discord


def log_dm(ev, message):
    author_text = f'{message.author.name}#{message.author.discriminator} [{message.author.id}]'
    ev.log.info(f'DM From {author_text}: {message.content}')


async def dm_detection(ev, message):
    if not message.guild:
        pfx = ev.bot.get_prefix(message)
        if not message.content.startswith(pfx):
            log_dm(ev, message)
            pm_response = discord.Embed(color=0x3B88C3, title=f'ℹ Type `{pfx}help` for information!')
            await message.channel.send(None, embed=pm_response)
        else:
            cmd_name = message.content.split(' ')[0][len(pfx):].lower()
            if cmd_name in ev.bot.modules.alts:
                cmd_name = ev.bot.modules.alts[cmd_name]
            if cmd_name not in ev.bot.modules.commands:
                log_dm(ev, message)
                pm_response = discord.Embed(color=0x696969, title='🔍 Not A Recognized Command')
                await message.channel.send(None, embed=pm_response)

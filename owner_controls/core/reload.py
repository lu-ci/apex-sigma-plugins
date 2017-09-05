import discord


async def reload(cmd, message, args):
    cmd.log.info('---------------------------------')
    cmd.log.info('Reloading all modules...')
    cmd.bot.ready = False
    response = discord.Embed(color=0xF9F9F9, title='⚗ Reloading all modules...')
    load_status = await message.channel.send(embed=response)
    cmd.bot.init_modules()
    cmd_count = len(cmd.bot.modules.commands)
    ev_count = 0
    for key in cmd.bot.modules.events:
        event_group = cmd.bot.modules.events[key]
        ev_count += len(event_group)
    load_done_resonse = discord.Embed(color=0x77B255, title=f'✅ Loaded {cmd_count} Commands and {ev_count} Events.')
    await load_status.edit(embed=load_done_resonse)
    cmd.bot.ready = True
    cmd.log.info(f'Loaded {cmd_count} commands and {ev_count} events.')
    cmd.log.info('---------------------------------')


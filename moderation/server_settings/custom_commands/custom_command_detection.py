from sigma.core.mechanics.permissions import GlobalCommandPermissions
from sigma.core.utilities.data_processing import command_message_parser

async def custom_command_detection(ev, message):
    if message.guild:
        prefix = ev.bot.get_prefix(message)
        if message.content.startswith(prefix):
            cmd = message.content[len(prefix):].lower().split()[0]
            if cmd not in ev.bot.modules.commands:
                perms = GlobalCommandPermissions(ev, message)
                if perms.permitted:
                    custom_commands = ev.db.get_guild_settings(message.guild.id, 'CustomCommands')
                    if custom_commands is None:
                        custom_commands = {}
                    if cmd in custom_commands:
                        cmd_text = custom_commands[cmd]
                        response = command_message_parser(message, cmd_text)
                        await message.channel.send(response)

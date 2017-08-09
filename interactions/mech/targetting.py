import discord


def get_target(message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        if args:
            lookup = ' '.join(args)
            target = discord.utils.find(lambda x: x.name.lower() == lookup.lower(), message.guild.members)
            if not target:
                for mem in message.guild.members:
                    if mem.nick:
                        if mem.nick.lower() == lookup.lower():
                            target = mem
                            break
        else:
            target = None
    return target


def make_footer(cmd, item):
    if item['auth']:
        uid = item['auth']
        user = discord.utils.find(lambda x: x.id == uid, cmd.bot.get_all_members())
        if user:
            username = user.name
        else:
            username = 'Unknown User'
    else:
        username = 'Unknown User'
    sid = item['sid']
    srv = discord.utils.find(lambda x: x.id == sid, cmd.bot.guilds)
    if srv:
        servername = srv.name
    else:
        servername = 'Unknown Server'
    footer = f'Submitted by {username} from {servername}.'
    return footer

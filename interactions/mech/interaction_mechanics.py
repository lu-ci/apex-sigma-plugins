import secrets
import discord


def grab_interaction(db, intername):
    interactions = db[db.db_cfg.database]['Interactions'].find({'Name': intername})
    interactions = list(interactions)
    choice = secrets.choice(interactions)
    return choice


def get_target(message):
    if message.mentions:
        target = message.mentions[0]
    else:
        if message.content:
            lookup = ' '.join(message.content.split(' ')[1:])
            target = discord.utils.find(
                lambda x: x.display_name.lower() == lookup.lower() or x.name.lower() == lookup.lower(),
                message.guild.members)
            if not target:
                target = discord.utils.find(
                    lambda x: x.name.lower() == lookup.lower() or x.name.lower() == lookup.lower(),
                    message.guild.members)
        else:
            target = None
    return target


def make_footer(cmd, item):
    if item['UserID']:
        uid = item['UserID']
        user = discord.utils.find(lambda x: x.id == uid, cmd.bot.get_all_members())
        if user:
            username = user.name
        else:
            username = 'Unknown User'
    else:
        username = 'Unknown User'
    sid = item['ServerID']
    srv = discord.utils.find(lambda x: x.id == sid, cmd.bot.guilds)
    if srv:
        servername = srv.name
    else:
        servername = 'Unknown Server'
    footer = f'Submitted by {username} from {servername}.'
    return footer

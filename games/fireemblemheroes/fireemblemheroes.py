import discord
import pymongo
from fuzzywuzzy import fuzz, process
from sigma.core.mechanics.config import Configuration

# Set up external DB connection
db_cfg = Configuration().db_cfg_data
if db_cfg['auth']:
    db_address = f"mongodb://{db_cfg['username']}:{db_cfg['password']}"
    db_address += f"@{db_cfg['host']}:{db_cfg['port']}/"
else:
    db_address = f"mongodb://{db_cfg['host']}:{db_cfg['port']}/"

# Iterate through data in the database and build an index for fuzzy searching
db = pymongo.MongoClient(db_address)
db = db.get_database(db_cfg['database']).get_collection('FEHData')
index = {}
for record in db.find():
    index[record['id']] = record['id']
    try:
        for alias in record['alias']:
            index[alias] = record['id']
    except KeyError:
        pass


# Looks up an index and queries the data from DB
def lookup(query):
    result = None
    if index:
        matches = process.extract(query, index.keys(), scorer=fuzz.ratio)
        # Hack to properly pick out + variants of weapons since scorer seem to ignore the +
        if query[-1] == '+':
            for match in matches:
                if match[0].find('+') != -1:
                    result = match[0]
                    break
        else:
            result = matches[0][0]
        result = db.find_one({'id': index[result]})
    return result


def get_specified_rarity(string):
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for index, character in enumerate(string):
        if character in numbers:
            return int(character)
    return False


# Embed colors
colors = {
    'Blue':    0x2763D8,
    'Red':     0xD12644,
    'Green':   0x0B9D27,
    'Neutral': 0x4E6971
}

# Icons to go in the embed footer
movetype_icon = {
    'Infantry': 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/4/45/Icon_Move_Infantry.png',
    'Flying':   'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/7/73/Icon_Move_Flying.png',
    'Armored':  'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/8/80/Icon_Move_Armored.png',
    'Cavalry':  'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/9/9f/Icon_Move_Cavalry.png',
}

# Icons to go in the author field
weapontype_icon = {
    'Red': {
        'Sword': 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/4/47/Icon_Class_Red_Sword.png',
        'Tome': 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/8/8a/Icon_Class_Red_Tome.png',
        'Breath': 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/2/2f/Icon_Class_Red_Beast.png'
    },
    'Blue': {
        'Lance': 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/archive/6/60/20170315235744!Icon_Class_Blue_Lance.png',
        'Tome': 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/archive/8/8e/20170315235956%21Icon_Class_Blue_Tome.png',
        'Breath': 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/archive/3/30/20170315235658%21Icon_Class_Blue_Beast.png'
    },
    'Green': {
        'Axe': 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/6/6e/Icon_Class_Green_Axe.png',
        'Tome': 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/7/75/Icon_Class_Green_Tome.png',
        'Breath': 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/d/d7/Icon_Class_Green_Beast.png'
    },
    'Neutral': {
        'Staff': 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/c/ca/Icon_Class_Neutral_Staff.png',
        'Bow': 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/2/24/Icon_Class_Neutral_Bow.png',
        'Dagger': 'https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/d/da/Icon_Class_Neutral_Shuriken.png'
    }
}


async def fireemblemheroes(cmd, message, args):
    args = list(filter(lambda a: a != '', args))  # strip spaces from args

    response = discord.Embed()
    if args:
        query = ' '.join(args).lower()
        record = lookup(query)
        if record:
            if record['type'] == 'hero':
                response.set_author(name=f"{record['name']}: {record['title']}",
                                    url=record['url'],
                                    icon_url=weapontype_icon[record['color']][record['weapon type']])
                response.set_thumbnail(url=record['icon'])
                response.colour = colors[record['color']]
                response.set_footer(icon_url=movetype_icon[record['movement type']],
                                    text=f"{record['rarity']} | {record['color']} {record['weapon type']}")

                rarity = get_specified_rarity(args[0])
                if not rarity:
                    # User did not specify rarity, output hero skills
                    response.description = record['bio']
                    for field in ['weapons', 'assists', 'specials', 'passives']:
                        if record[field]:
                            response.add_field(name=field.capitalize(), value=record[field], inline=False)
                else:
                    # User did specify rarity, output hero stats instead
                    # Check inputted rarity
                    if rarity < 1 or rarity > 5 or rarity is False or str(rarity) not in record['stats'].keys():
                        # If specified rarity is not in 1-5⭐ range or not specified at all or doesn't exist
                        rarity = '5'
                    else:
                        # Cast to string since dict keys are required to be strings
                        rarity = str(rarity)
                    # Add fields with stats
                    for stat_type in ['base', 'max']:
                        stats = record['stats'][rarity][stat_type]
                        stats = '\n'.join([f'**{key}**: {value}' for key, value in stats])
                        response.add_field(name=f'{rarity}\★ {stat_type} stats:', value=stats)
                    # Add BST to the footer
                    response._footer['text'] += ' | BST: ' + str(record['bst'][rarity])
            elif record['type'] == 'weapon':
                response.set_author(name=record['name'],
                                    url=record['url'],
                                    icon_url=weapontype_icon[record['color']][record['weapon type']])
                response.set_thumbnail(url=record['icon'])
                response.colour = colors[record['color']]
                stats = {
                    'Might': record['might'],
                    'Range': record['range'],
                    'SP Cost': record['sp cost'],
                    "Exclusive": 'Yes' if record['exclusive'] else 'No'
                }
                response.add_field(name='Stats', value='\n'.join([f'**{key}**: {stats[key]}' for key in stats]))
                if record['special effect']:
                    response.add_field(name='Special Effect', value=record['special effect'])
                if record['heroes with']:
                    response.add_field(name=f"List of heroes with {record['name']}", value=record['heroes with'])
                if record['see also']:
                    response.set_footer(text=f"See also: {record['see also']}")
            elif record['type'] == 'assist':
                response.set_author(name=record['name'], url=record['url'],
                                    icon_url='https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/9/9a/Icon_Skill_Assist.png?version=b76835fe03565ecdbe6296733e152b64')
                response.colour = 0x05DEBB
                stats = {
                    'Range': record['range'],
                    'SP Cost': record['sp cost'],
                    "Inherit Restriction": record['inherit restriction']
                }
                response.add_field(name='Stats', value='\n'.join([f'**{key}**: {stats[key]}' for key in stats]))
                response.add_field(name='Effect', value=record['effect'])
                response.add_field(name=f"List of heroes with {record['name']}", value=record['heroes with'])
            elif record['type'] == 'special':
                response.set_author(name=record['name'], url=record['url'],
                                    icon_url='https://feheroes.gamepedia.com/media/feheroes.gamepedia.com/2/25/Icon_Skill_Special.png?version=6c0491d6fb19447285026f367d5e2257')
                response.colour = 0xE29DE7
                stats = {
                    'Cooldown': record['cooldown'],
                    'SP Cost': record['sp cost'],
                    "Inherit Restriction": record['inherit restriction']
                }
                response.add_field(name='Stats', value='\n'.join([f'**{key}**: {stats[key]}' for key in stats]), inline=False)
                response.add_field(name='Effect', value=record['effect'], inline=False)
                response.add_field(name=f"List of heroes with {record['name']}", value=record['heroes with'])
            elif record['type'] == 'passive':
                icon = record['icon']
                response.set_author(name=record['name'], url=record['url'],
                                    icon_url=icon)
                response.set_thumbnail(url=icon)
                response.colour = colors['Neutral']

                stats = {'Passive Type': record['passive type']}
                if record['passive type'] != 'S':
                    stats['SP Cost'] = record['sp cost']
                    stats['Inherit Restriction'] = record['inherit restriction']
                response.add_field(name='Stats', value='\n'.join([f'**{key}**: {stats[key]}' for key in stats]), inline=False)
                response.add_field(name='Effect', value=record['effect'])
                if record['heroes with']:
                    response.add_field(name=f"List of heroes with {record['name']}", value=record['heroes with'])
                if record['see also']:
                    response.set_footer(text=f"See also: {record['see also']}")
        else:
             response.title = '🔍 No results.'
             response.colour = 0x696969
    else:
        response.title = '❗ Nothing inputted.'
        response.colour = 0xBE1931

    await message.channel.send(embed=response)

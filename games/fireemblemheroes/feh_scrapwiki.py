import aiohttp
import re
import json
from lxml import html
import wikitextparser as wtp
from datetime import datetime
import pymongo
from sigma.core.mechanics.config import Configuration

# Set up external DB connection
db_cfg = Configuration().db_cfg_data
if db_cfg['auth']:
    db_address = f"mongodb://{db_cfg['username']}:{db_cfg['password']}"
    db_address += f"@{db_cfg['host']}:{db_cfg['port']}/"
else:
    db_address = f"mongodb://{db_cfg['host']}:{db_cfg['port']}/"

db = pymongo.MongoClient(db_address)
db = db.get_database(db_cfg['database'])
wiki = db.get_collection('FEHWikiCache')
db = db.get_collection('FEHData')

wiki_url = 'https://feheroes.gamepedia.com'
#db = pymongo.MongoClient().get_database('yueri').get_collection('feh_data')
#wiki = pymongo.MongoClient().get_database('yueri').get_collection('feh_wiki_raw')
NO_CACHE = False
SKIP_BIO = False
VERBOSE = False


aliases = {
    'hero': {
        # Performing Arts
        'Azura (Performing Arts)':   ['PA Azura', 'Axura', 'Green Azura', 'Dark Azura'],
        'Inigo (Performing Arts)':   ['PA Inigo', 'Inigo'],
        'Olivia (Performing Arts)':  ['PA Olivia', 'Performing Arts Olivia', 'Dagger Olivia'],
        'Shigure (Performing Arts)': ['PA Shigure', 'Shigure'],
        # Brave Heroes / Choose your legend
        'Ike (Brave Heroes)':    ['BH Ike',    'CYL Ike',    'Brave Ike', 'Bike', 'Green Ike', 'Axe Ike'],
        'Lucina (Brave Heroes)': ['BH Lucina', 'CYL Lucina', 'Brave Lucina', 'Lancina'],
        'Lyn (Brave Heroes)':    ['BH Lyn',    'CYL Lyn',    'Brave Lyn', 'Bow Lyn', 'Archer Lyn', 'Lyn on a horse'],
        'Roy (Brave Heroes)':    ['BH Roy',    'CYL Roy',    'Brave Roy', 'Roy on a horse'],
        # Nohrian Summer
        'Corrin (F) (Nohrian Summer)': ['Summer Corrin'],
        'Elise (Nohrian Summer)':      ['Summer Elise'],
        'Leo (Nohrian Summer)':        ['Summer Leo'],
        'Xander (Nohrian Summer)':     ['Summer Xander'],
        # Ylissean Summer
        'Frederick (Ylissean Summer)':    ['Summer Frederick'],
        'Gaius (Ylissean Summer)':        ['Summer Gaius'],
        'Robin (F) (Ylissean Summer)':    ['Summer Robin'],
        'Tiki (Adult) (Ylissean Summer)': ['Summer Tiki'],
        # Bridal Blessing
        'Caeda (Bridal Blessings)':     ['Bride Caeda'],
        'Charlotte (Bridal Blessings)': ['Bride Charlotte'],
        'Cordelia (Bridal Blessings)':  ['Bride Cordelia', 'Bridelia', 'Bow Cordelia', 'Archer Cordelia'],
        'Lyn (Bridal Blessings)':       ['Bride Lyn', 'Staff Lyn', 'Healer Lyn'],
        # Spring Festival
        'Camilla (Spring Festival)': ['Bunny Camilla', 'Spring Camilla'],
        'Chrom (Spring Festival)':   ['Bunny Chrom',   'Spring Chrom'],
        'Lucina (Spring Festival)':  ['Bunny Lucina',  'Spring Lucina'],
        'Xander (Spring Festival)':  ['Bunny Xander',  'Spring Xander'],
        # Shorthands and not
        'Black Knight': ['BK'],
        'Reinhardt': ['Magic is everything'],
        'Takumi': ['Tako', 'Taco'],
        # Rest
        'Corrin (F)': ['Female Corrin'],
        'Corrin (M)': ['Male Corrin'],
        'Robin (F)': ['Female Robin'],
        'Robin (M)': ['Male Robin'],
        'Tiki (Adult)': ['Tiki', 'Adult Tiki'],
        'Tiki (Young)': ['Young Tiki'],
        'Marth (Masked)': ['Masked Lucina', 'Definitely not Lucina']
    },
    'weapon': {
        # Red Swords
        'Fólkvangr': ['Folkvangr'],
        # Red Tomes
        'Rauðrblade': ['Raudrblade'],
        'Rauðrblade+': ['Raudrblade+'],
        'Rauðrowl': ['Raudrowl'],
        'Rauðrowl+': ['Raudrowl+'],
        'Rauðrraven': ['Raudrraven'],
        'Rauðrraven+': ['Raudrraven+'],
        'Rauðrwolf': ['Raudrwolf'],
        'Rauðrwolf+': ['Raudrwolf+'],
        # Blue Lance
        'Geirskögul': ['Geirskogul'],
        # Blue Tomes
        'Blárblade': ['Blarblade'],
        'Blárblade+': ['Blarblade+'],
        'Blárowl': ['Blarowl'],
        'Blárowl+': ['Blarowl+'],
        'Blárraven': ['Blarraven'],
        'Blárraven+': ['Blarraven+'],
        'Blárwolf': ['Blarwolf'],
        'Blárwolf+': ['Blarwolf+'],
        'Dire Thunder': ['Brave Tome'],
        'Valaskjálf': ['Valaskjalf'],
        # Green Axe
        'Nóatún': ['Noatun'],
        'Urðr': ['Urdr', 'Fate'],
        # Green Tome
        'Élivágar': ['Elivagar'],
    }
}

# Used in calculating max stats
growth_values = {
    #*    0   1   2   3   4   5   6   7   8   9  10  11  12  13
    '5': [8, 10, 13, 15, 17, 19, 22, 24, 26, 28, 30, 33, 35, 37],
    '4': [8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 31, 33, 35],
    '3': [7,  9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33],
    '2': [7,  8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 26, 28],
    '1': [6,  8,  9, 11, 13, 14, 16, 18, 19, 21, 23, 24, 26]
}


def format_link(page, raw=False, api=False, sections='0'):
    url = '/' + page if page[0] != '/' else page
    if raw:
        url += '?action=raw'
    elif api:
        url = f'/api.php?action=ask&format=json&query={page}'
    else:
        url = f'''
        /api.php
        ?action=mobileview
        &format=json
        &sections={sections}
        &notransform=true
        &onlyrequestedsections=true
        &page={page}
        '''
        url = ''.join(url.split('\n        '))
    return url


async def get_page(url):
    cache = wiki.find_one({'url': url})
    if cache and not NO_CACHE:
        return cache
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(wiki_url + url) as data_response:
                data = await data_response.read()
        record = {
            'url': url,
            'data': data,
            'timestamp': datetime.utcnow().timestamp()
        }
        wiki.insert_one(record)
        return record


def get_template(markup, name):
    for template in markup.templates:
        if template.name.strip() == name.strip():
            return template
    return None


def get_argument(template, name):
    for argument in template.arguments:
        if argument.name.strip() == name.strip():
            return argument
    return None


def get_value(*args):
    if len(args) == 1:
        raise Exception('Not enough arguments')
    elif len(args) == 2:
        template = args[0]
        argument = args[1]
    elif len(args) == 3:
        markup = args[0]
        template = args[1]
        argument = args[2]
    else:
        raise Exception('Too much arguments')
    if len(args) == 3:
        template = get_template(markup, template)
    argument = get_argument(template, argument)
    if argument:
        value = argument.value
        if isinstance(value, str):
            value = value.strip()
            if value == '':
                value = None
        return value
    else:
        return None


def get_range(markup, template, argument, starting_from=1):
    indexes = []
    template = get_template(markup, template)
    if not template:
        return indexes
    while get_argument(template, argument + str(starting_from)):
        index = get_argument(template, argument + str(starting_from))
        if index:
            indexes.append(str(starting_from))
        starting_from += 1
    return indexes


def parse_bio(bio):
    if bio:
        for match in re.findall(r'\[{2}[a-zA-Z\s\(\)\|]+\]{2}', bio):
            link = match[2:-2].split('|')
            if len(link) > 1:
                text = link[1]
            else:
                text = link[0]
            link = link[0].replace(' ', '_')
            bio = bio.replace(match, f"[{text}]({wiki_url + '/' + link})")
        bio = bio.strip().replace('))', '\\))')  # Escape the links
    return bio


def parse_rarity(summon_rarities, reward_rarities):
    if summon_rarities:
        if len(summon_rarities) > 1:
            rarity = f'{summon_rarities[0]}★ - {summon_rarities[-1]}★'
        else:
            rarity = f'{summon_rarities[0]}★'
    elif reward_rarities:
        if len(reward_rarities) > 1:
            rarity = f'{reward_rarities[0]}★ - {reward_rarities[-1]}★'
        else:
            rarity = f'{reward_rarities[0]}★'
    else:
        rarity = 'N/A'
    return rarity


# Sort stats in HP - ATK - SPD - DEF - RES order
# Input stats format is [['HP', int], ['ATK', int], ['SPD', int], ['DEF', int], ['RES', int]]
def sort_stats(stats):
    keys = [stat[0] for stat in stats]
    sorted_stats = []
    for stat in ['HP', 'ATK', 'SPD', 'DEF', 'RES']:
        sorted_stats.append([stat, stats[keys.index(stat)][1]])
    return sorted_stats


def calculate_base_stats_down(stats, is_odd=True):
    stats = sort_stats(stats)
    if not is_odd:
        # Decrease HP by one point if calculating from 5⭐ -> 4⭐ and 3⭐ -> 2⭐
        hp = stats[0][1] - 1
    else:
        hp = stats[0][1]
    rest = stats[1:]  # Step over HP
    if not is_odd:
        # Reverse the array to preserve ATT - SPD - DEF - RES order if values are tied
        rest = reversed(rest)
    rest = sorted(rest, key=lambda stat: stat[1], reverse=is_odd)  # Sort the stats
    # Decrease two lowest stats if calculating from 5⭐ -> 4⭐ and 3⭐ -> 2⭐
    # Decrease two highest stats if calculating from 4⭐ -> 3⭐ and 2⭐ -> 1⭐
    for index in range(0, 2):
        rest[index][1] -= 1
    # Return the array
    calculated_stats = rest
    calculated_stats.append(['HP', hp])
    calculated_stats = sort_stats(calculated_stats)
    return calculated_stats


# Calculate stats from 5⭐ -> 4⭐ and 3⭐ -> 2⭐
def calculate_base_stats_even(stats):
    return calculate_base_stats_down(stats, False)


# Calculate stats from 4⭐ -> 3⭐ and 2⭐ -> 1⭐
def calculate_base_stats_odd(stats):
    return calculate_base_stats_down(stats, True)


def calculate_max_stats(rarity, base, gp):
    max_stats = []
    for index, stat in enumerate(['HP', 'ATK', 'SPD', 'DEF', 'RES']):
        value = base[index][1] + growth_values[rarity][gp[index][1]]
        max_stats.append([stat, value])
    return max_stats


async def scrap_hero_data():
    heroes = {}
    # Parse hero list, primarily for icons
    url = format_link('Hero List')
    data = await get_page(url)
    data = json.loads(data['data'])
    data = data['mobileview']['sections'][0]['text']
    root = html.fromstring(data)
    hero_list_table = root.cssselect('table.wikitable')[0]
    hero_list = hero_list_table[8:]  # strip the header
    for row in hero_list:
        hero_id = row[1][0].text
        url = row[1][0].attrib['href']
        hero_name = re.sub(r'\([a-zA-Z\(\)\s]+\)', '', hero_id).strip()  # strip " (text)" from names

        icon = row[0][0][0].attrib['src'].split('?')[0].split('/')
        icon = '/'.join(icon[:5] + icon[6:-1])

        hero_record = {
            'type': 'hero',
            'id': hero_id,
            'url': wiki_url + url,
            'name': hero_name,
            'icon': icon

        }
        heroes[hero_id] = hero_record

    # Parse heroes bio
    # They're not directly exposed to the API, gotta parse the pages one by one, FML
    for hero in heroes.keys():
        if SKIP_BIO:
            heroes[hero]['bio'] = None
        else:
            url = format_link(hero, raw=True)
            page = await get_page(url)
            page = wtp.parse(page['data'])
            hero_page_text = get_template(page, 'HeroPageText')
            bio = get_value(hero_page_text, 'Background')
            bio = parse_bio(bio)
            heroes[hero]['bio'] = bio

    # Query pretty much the rest
    query = '''
    [[Category:Heroes]]
    |?Title
    |?WeaponType
    |?MoveType
    |?SummonRarities
    |?RewardRarities
    |?Has weapon1=weapon1
    |?Has weapon2=weapon2
    |?Has weapon3=weapon3
    |?Has weapon4=weapon4
    |?Has weapon1 unlock=weapon1Unlock
    |?Has weapon2 unlock=weapon2Unlock
    |?Has weapon3 unlock=weapon3Unlock
    |?Has weapon4 unlock=weapon4Unlock
    |?Has assist1=assist1
    |?Has assist2=assist2
    |?Has assist3=assist3
    |?Has assist4=assist4
    |?Has assist1 unlock=assist1Unlock
    |?Has assist2 unlock=assist2Unlock
    |?Has assist3 unlock=assist3Unlock
    |?Has assist4 unlock=assist4Unlock
    |?Has special1=special1
    |?Has special2=special2
    |?Has special3=special3
    |?Has special4=special4
    |?Has special1 unlock=special1Unlock
    |?Has special2 unlock=special2Unlock
    |?Has special3 unlock=special3Unlock
    |?Has special4 unlock=special4Unlock
    |?Has passiveA1=passiveA1
    |?Has passiveA2=passiveA2
    |?Has passiveA3=passiveA3
    |?Has passiveB1=passiveB1
    |?Has passiveB2=passiveB2
    |?Has passiveB3=passiveB3
    |?Has passiveC1=passiveC1
    |?Has passiveC2=passiveC2
    |?Has passiveC3=passiveC3
    |?Has passiveA1 unlock=passiveA1Unlock
    |?Has passiveA2 unlock=passiveA2Unlock
    |?Has passiveA3 unlock=passiveA3Unlock
    |?Has passiveB1 unlock=passiveB1Unlock
    |?Has passiveB2 unlock=passiveB2Unlock
    |?Has passiveB3 unlock=passiveB3Unlock
    |?Has passiveC1 unlock=passiveC1Unlock
    |?Has passiveC2 unlock=passiveC2Unlock
    |?Has passiveC3 unlock=passiveC3Unlock
    |?Has Lv1_R5_HP_Neut=baseHP
    |?Has Lv1_R5_ATK_Neut=baseATK
    |?Has Lv1_R5_SPD_Neut=baseSPD
    |?Has Lv1_R5_DEF_Neut=baseDEF
    |?Has Lv1_R5_RES_Neut=baseRES
    |?Has HP Growth Point=gpHP
    |?Has Atk Growth Point=gpATK
    |?Has Spd Growth Point=gpSPD
    |?Has Def Growth Point=gpDEF
    |?Has Res Growth Point=gpRES
    |?Has Lv1_R1_HP_Neut=r1
    |?Has Lv1_R2_HP_Neut=r2
    |?Has Lv1_R3_HP_Neut=r3
    |?Has Lv1_R4_HP_Neut=r4
    |limit=500
    '''
    query = ''.join(query.split('\n    '))
    query = format_link(query, api=True)
    query = await get_page(query)
    query = json.loads(query['data'])
    query = query['query']['results']
    for hero in query:
        heroes[hero]['title'] = query[hero]['printouts']['Title'][0]
        heroes[hero]['color'] = query[hero]['printouts']['WeaponType'][0].split(' ')[0]
        heroes[hero]['weapon type'] = query[hero]['printouts']['WeaponType'][0].split(' ')[1]
        heroes[hero]['movement type'] = query[hero]['printouts']['MoveType'][0]
        summon_rarities = query[hero]['printouts']['SummonRarities']
        reward_rarities = query[hero]['printouts']['RewardRarities']
        heroes[hero]['rarity'] = parse_rarity(summon_rarities, reward_rarities)

        skills = {}
        # Parse weapons, assists and specials
        for skill_type in ['weapon', 'assist', 'special']:
            skills[skill_type + 's'] = []
            for tier in range(1, 5):
                tier = str(tier)
                skill = query[hero]['printouts'][skill_type + tier][0]['fulltext'] \
                    if query[hero]['printouts'][skill_type + tier] else None
                unlock = query[hero]['printouts'][skill_type + tier + 'Unlock']

                if skill and unlock:
                    skill += f' ({unlock[0]}\★)'
                if skill:
                    skills[skill_type + 's'].append(skill)
            skills[skill_type + 's'] = ', '.join(skills[skill_type + 's'])

        # Parse passives
        skills['passives'] = {}
        for passive_type in ['A', 'B', 'C']:
            skills['passives'][passive_type] = []
            for tier in range(1, 4):
                tier = str(tier)
                skill = query[hero]['printouts']['passive' + passive_type + tier][0] \
                    if query[hero]['printouts']['passive' + passive_type + tier] else None
                unlock = query[hero]['printouts']['passive' + passive_type + tier + 'Unlock']

                if skill and unlock:
                    skill += f' ({unlock[0]}\★)'
                if skill:
                    skills['passives'][passive_type].append(skill)
        skills['passives'] = '\n'.join([f"`{passive_type}` | {', '.join(skills['passives'][passive_type])}"
                                        for passive_type in skills['passives'] if skills['passives'][passive_type]])

        # Save fetched data to the record
        heroes[hero]['weapons'] = skills['weapons']
        heroes[hero]['assists'] = skills['assists']
        heroes[hero]['specials'] = skills['specials']
        heroes[hero]['passives'] = skills['passives']

        # Parse base stats, growth points and calculate the rest
        if not query[hero]['printouts']['baseHP']:
            # Exception handler for Bruno and Veronica
            stats = None
        else:
            stats = {
                '5': {'base': [], 'max': []},
            }
            for stat_type in ['base', 'gp']:
                values = []
                for stat in ['HP', 'ATK', 'SPD', 'DEF', 'RES']:
                    value = int(query[hero]['printouts'][stat_type + stat][0])
                    values.append([stat, value])
                if stat_type == 'base':
                    stats['5'][stat_type] = values
                else:
                    gp = values

            # Calculate max 5⭐ stats
            stats['5']['max'] = calculate_max_stats('5', stats['5']['base'], gp)

            # Parse rarities that hero available in
            rarities = []
            for rarity in ['1', '2', '3', '4']:  # Always available in 5⭐
                value = query[hero]['printouts']['r' + rarity]
                if value:
                    rarities.append(rarity)

            # Calculate base and max stats for these rarities
            for rarity in reversed(rarities):
                # Calculate base stats
                previous = str(int(rarity) + 1)
                previous = stats[previous]['base']
                stats[rarity] = {}
                if int(rarity) % 2:
                    values = calculate_base_stats_odd(previous)
                else:
                    values = calculate_base_stats_even(previous)
                stats[rarity] = {}
                stats[rarity]['base'] = values
                # Calculate max stats
                stats[rarity]['max'] = calculate_max_stats(rarity, stats[rarity]['base'], gp)

            # Save stats in the record
            heroes[hero]['stats'] = stats

            # Calculate BST for each rarity
            heroes[hero]['bst'] = {}
            for rarity in stats:
                total = 0
                for stat in stats[rarity]['max']:
                    total += stat[1]
                heroes[hero]['bst'][rarity] = total

        # Inject aliases
        heroes[hero]['alias'] = aliases['hero'][hero] if hero in aliases['hero'].keys() else []
        if VERBOSE:
            print(heroes[hero])

    return heroes


async def scrap_weapon_data():
    weapons = {}
    plurarize = {
        'Sword': 'Swords',
        'Tome': 'Tomes',
        'Breath': 'Breaths',
        'Lance': 'Lances',
        'Axe': 'Axes',
        'Staff': 'Staves',
        'Bow': 'Bows',
        'Dagger': 'Daggers'
    }
    weapon_types = {
        'Red': ['Sword', 'Tome', 'Breath'],
        'Blue': ['Lance', 'Tome', 'Breath'],
        'Green': ['Axe', 'Tome', 'Breath'],
        'Neutral': ['Staff', 'Bow', 'Dagger']
    }
    for color in weapon_types:
        for weapon_type in weapon_types[color]:
            category = plurarize[weapon_type]
            if weapon_type in ['Tome', 'Breath']:
                category = color + ' ' + category
            query = f'''
            [[Category:{category}]]
            |?name1
            |?might1
            |?range1
            |?cost1
            |?Is exclusive=exclusive
            |?effect1
            |limit=500
            '''
            query = ''.join(query.split('\n            '))
            query = format_link(query, api=True)
            query = await get_page(query)
            query = json.loads(query['data'])
            query = query['query']['results']
            for weapon_name in query:
                special_effect = query[weapon_name]['printouts']['Effect1'][0] if query[weapon_name]['printouts']['Effect1'] else None
                if special_effect:
                    # Strip [[]] tags
                    special_effect = special_effect.replace('<br>', ' ')
                    special_effect = special_effect.split(' ')
                    special_effect = [part for part in special_effect if part[:2] != '[[' and part[-2:] != ']]']
                    special_effect = ' '.join(special_effect)

                # Scrapping images
                url = format_link(weapon_name)
                page = await get_page(url)
                page = page['data']
                page = json.loads(page)
                page = page['mobileview']['sections'][0]['text']
                root = html.fromstring(page)
                images = root.cssselect('.hero-infobox a img')
                image = images[0].attrib['src'].split('?')[0]

                heroes_with = []
                # Query the heroes with list
                # Sit back because it's gonna take a while
                for tier in ['4', '3', '2', '1']:
                    escaped_name = weapon_name.replace(' ', '_').replace('+', '%2B')
                    subquery = f"[[Category:Heroes]][[Has weapon{tier}::{escaped_name} ]]|?Has weapon{tier} unlock=weapon{tier}Unlock"
                    subquery = format_link(subquery, api=True)
                    subquery = await get_page(subquery)
                    subquery = json.loads(subquery['data'])
                    subquery = subquery['query']['results']
                    if subquery:
                        for hero in subquery:
                            unlock = subquery[hero]['printouts'][f'weapon{tier}Unlock'][0] \
                                if subquery[hero]['printouts'][f'weapon{tier}Unlock'] else None
                            if unlock:
                                hero += f' ({unlock}\★)'
                            heroes_with.append(hero)
                        break

                # Inject aliases
                alias = aliases['weapon'][weapon_name] if weapon_name in aliases['weapon'].keys() else []

                weapon = {
                    'type': 'weapon',
                    'id': weapon_name,
                    'name': weapon_name,
                    'color': color,
                    'weapon type': weapon_type,
                    'url': wiki_url + '/' + weapon_name.replace(' ', '_'),
                    'icon': image,
                    'might': int(query[weapon_name]['printouts']['Might1'][0]),
                    'range': int(query[weapon_name]['printouts']['Range1'][0]),
                    'sp cost': int(query[weapon_name]['printouts']['Cost1'][0]),
                    'exclusive': True if query[weapon_name]['printouts']['exclusive'] else False,
                    'special effect': special_effect,
                    'heroes with': ', '.join(heroes_with),
                    'alias': alias
                }
                weapons[weapon_name] = weapon

    # Cross references for + weapons
    for weapon in weapons:
        if weapon + '+' in weapons.keys():
            weapons[weapon]['see also'] = weapon + '+'
            weapons[weapon + '+']['see also'] = weapon
        else:
            weapons[weapon]['see also'] = None
        if VERBOSE:
            print(weapons[weapon])

    return weapons


async def scrap_assist_data():
    assists = {}
    query = '''
    [[Category:Assists]]
    |?name1
    |?range1
    |?effect1
    |?cost1
    |?Has weapon restriction=wpnRestrict
    |?Is exclusive=exclusive
    |limit=100
    '''
    query = ''.join(query.split('\    '))
    query = format_link(query, api=True)
    query = await get_page(query)
    query = json.loads(query['data'])
    query = query['query']['results']
    for assist in query:
        effect = query[assist]['printouts']['Effect1'][0].replace('<br>', ' ')
        inherit_restriction = query[assist]['printouts']['wpnRestrict']
        if inherit_restriction:
            inherit_restriction = inherit_restriction[0]
        else:
            if query[assist]['printouts']['exclusive'][0] == 't':
                inherit_restriction = 'Is exclusive'
            else:
                raise Exception
        heroes_with = []
        escaped_name = assist.replace(' ', '_')
        for tier in ['1', '2', '3']:
            subquery = f"[[Category:Heroes]][[Has assist{tier}::{escaped_name} ]]|?Has assist{tier} unlock=assist{tier}Unlock"
            subquery = format_link(subquery, api=True)
            subquery = await get_page(subquery)
            subquery = json.loads(subquery['data'])
            subquery = subquery['query']['results']
            if subquery:
                for hero in subquery:
                    unlock = subquery[hero]['printouts'][f'assist{tier}Unlock']
                    if unlock:
                        hero += f' ({unlock[0]}★)'
                    heroes_with.append(hero)
                break
        heroes_with = ', '.join(heroes_with)

        assists[assist] = {
            'type': 'assist',
            'id': assist,
            'name': assist,
            'url': wiki_url + '/' + assist.replace(' ', '_'),
            'range': query[assist]['printouts']['Range1'][0],
            'effect': effect,
            'sp cost': query[assist]['printouts']['Cost1'][0],
            'inherit restriction': inherit_restriction,
            'heroes with': heroes_with
        }
        if VERBOSE:
            print(assists[assist])
    return assists


async def scrap_special_data():
    specials = {}
    query = '''
    [[Category:Specials]]
    |?name1
    |?cooldown1
    |?effect1
    |?cost1
    |?Has weapon restriction=wpnRestrict
    |?Has mvmt restriction=mvmtRestrict
    |?Is exclusive=exclusive
    |limit=100
    '''
    query = ''.join(query.split('\    '))
    query = format_link(query, api=True)
    query = await get_page(query)
    query = json.loads(query['data'])
    query = query['query']['results']
    for special in query:
        effect = query[special]['printouts']['Effect1'][0].replace('<br>', ' ')
        inherit_restriction = query[special]['printouts']['wpnRestrict']
        if inherit_restriction:
            inherit_restriction = inherit_restriction[0].replace('Exclusive', 'Is exclusive')
        else:
            is_exclusive = query[special]['printouts']['exclusive']
            if is_exclusive:
                if is_exclusive[0] == 't':
                    inherit_restriction = 'Is exclusive'
                else:
                    inherit_restriction = None
            else:
                inherit_restriction = None

        heroes_with = []
        escaped_name = special.replace(' ', '_')
        for tier in ['1', '2', '3']:
            subquery = f"[[Category:Heroes]][[Has special{tier}::{escaped_name} ]]|?Has special{tier} unlock=special{tier}Unlock"
            subquery = format_link(subquery, api=True)
            subquery = await get_page(subquery)
            subquery = json.loads(subquery['data'])
            subquery = subquery['query']['results']
            if subquery:
                for hero in subquery:
                    unlock = subquery[hero]['printouts'][f'special{tier}Unlock']
                    if unlock:
                        hero += f' ({unlock[0]}★)'
                    heroes_with.append(hero)
                break
        heroes_with = ', '.join(heroes_with)

        specials[special] = {
            'type': 'special',
            'id': special,
            'name': special,
            'url': wiki_url + '/' + special.replace(' ', '_'),
            'cooldown': query[special]['printouts']['Cooldown1'][0],
            'effect': effect,
            'sp cost': query[special]['printouts']['Cost1'][0],
            'inherit restriction': inherit_restriction,
            'heroes with': heroes_with
        }
        if VERBOSE:
            print(specials[special])
    return specials


async def scrap_passive_data():
    passives = {}
    query = format_link('Passives', sections='1|2|3|4')
    query = await get_page(query)
    query = json.loads(query['data'])
    sections = query['mobileview']['sections']

    # Inject passive type into each section
    for index, passive_type in enumerate(['A', 'B', 'C', 'S']):
        sections[index]['passive type'] = passive_type

    for section in sections:
        table = html.fromstring(section['text']).cssselect('table')[0]
        for row in table[5:]:  # Skip the heading
            name = row[1][0].text.strip()

            heroes_with = []
            passive_type = section['passive type']
            escaped_name = name.replace('+', '%2B')
            if passive_type != 'S':  # Seals are universal
                subquery = None
                if name[-1] in ['1', '2', '3']:
                    tier = name[-1]
                else:
                    tier = '3'
                while not subquery:
                    subquery = f"[[Category:Heroes]][[Has passive{passive_type}{tier}::{escaped_name} ]]|?Has passive{passive_type}{tier} unlock=passive{passive_type}{tier}Unlock"
                    subquery = format_link(subquery, api=True)
                    subquery = await get_page(subquery)
                    subquery = json.loads(subquery['data'])
                    subquery = subquery['query']['results']
                    if subquery:
                        for hero in subquery:
                            unlock = subquery[hero]['printouts'][f'passive{passive_type}{tier}Unlock']
                            if unlock:
                                hero += f' ({unlock[0]}★)'
                            heroes_with.append(hero)
                        break
                    else:
                        tier = '1' if tier == '3' else str(int(tier) + 1)
            heroes_with = ', '.join(heroes_with)

            passives[name] = {
                'type': 'passive',
                'passive type': section['passive type'],
                'id': name,
                'name': name,
                'url': wiki_url + '/' + name.replace(' ', '_'),
                'icon': row[0][0][0].attrib['src'].split('?')[0],
                'effect': row[2].text.strip(),
                'sp cost': int(row[3].text) if row[3].text else row[3].text,
                'inherit restriction': row[4].text,
                'heroes with': heroes_with if heroes_with else None
            }

    # Add S to seal type if passive is available as a seal
    query = '[[Category:Passives]][[Has seal::true]]|?name1|?name2|?name3|limit=100'
    query = format_link(query, api=True)
    query = await get_page(query)
    query = json.loads(query['data'])['query']['results']
    for passive in query:
        for index in ['1', '2', '3']:
            name = query[passive]['printouts']['Name' + index][0] \
                if query[passive]['printouts']['Name' + index] else None
            if name:
                if passives[name]['passive type'] != 'S':
                    passives[name]['passive type'] += ', S'

    for passive in passives:
        see_also = []
        if passive[-1] in ['1', '2', '3']:
            prev_lvl = str(int(passive[-1]) - 1)
            next_lvl = str(int(passive[-1]) + 1)
            while prev_lvl != '0':
                prev_lvl_passive = passive[:-1] + prev_lvl
                exists = True if prev_lvl_passive in passives.keys() else False
                if exists:
                    see_also.append(prev_lvl_passive)
                prev_lvl = str(int(prev_lvl) - 1)
            while next_lvl != '4':
                next_lvl_passive = passive[:-1] + next_lvl
                exists = True if next_lvl_passive in passives.keys() else False
                if exists:
                    see_also.append(next_lvl_passive)
                next_lvl = str(int(next_lvl) + 1)

        # Add level-less alias to strongest passive
        # Armored Blow 3 -> Armored Blow
        alias = []
        if passive[-1] in ['1', '2', '3']:
            next_lvl = str(int(passive[-1]) + 1)
            next_lvl_passive = passive[:-1] + next_lvl
            exists = True if next_lvl_passive in passives.keys() else False
            if not exists:
                alias.append(passive[:-1].replace('+', '').strip())

        passives[passive]['see also'] = ', '.join(see_also) if see_also else None
        passives[passive]['alias'] = alias

        if VERBOSE:
            print(passives[passive])
    return passives

async def scrap_all():
    data = []
    data.append(await scrap_hero_data())
    data.append(await scrap_weapon_data())
    data.append(await scrap_assist_data())
    data.append(await scrap_special_data())
    data.append(await scrap_passive_data())
    return data


def insert_into_db(data):
    for items in data:
        for item_id in items:
            db.insert_one(items[item_id])

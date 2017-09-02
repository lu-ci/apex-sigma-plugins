import discord
import secrets
from sigma.core.utilities.data_processing import user_avatar

symbol_rewards = {
    9: '💎',
    8: '🔱',
    7: '💠',
    6: '🍁',
    5: '🍆',
    4: '☀',
    3: '🍌',
    2: '☢',
    1: '☎',
    0: '🔥'
}

rarity_rewards = {
    '💎': 500,
    '🔱': 200,
    '💠': 100,
    '🍁': 50,
    '🍆': 25,
    '☀': 20,
    '🍌': 15,
    '☢': 10,
    '☎': 5,
    '🔥': 1
}


def roll_symbol():
    rarities = {
        0: 0,
        1: 35000,
        2: 60000,
        3: 80000,
        4: 95000,
        5: 98000,
        6: 99100,
        7: 99600,
        8: 99850,
        9: 99950
    }
    roll = secrets.randbelow(100000)
    lowest = 0
    for rarity in rarities:
        if rarities[rarity] <= roll:
            lowest = rarity
        else:
            break
    return lowest


async def slots(cmd, message, args):
    currency_icon = cmd.bot.cfg.pref.currency_icon
    currency = cmd.bot.cfg.pref.currency
    current_kud = cmd.db.get_currency(message.author, message.guild)['current']
    if args:
        try:
            bet = abs(int(args[0]))
        except ValueError:
            bet = 10
    else:
        bet = 10
    if bet > 500:
        bet = 500
    if current_kud >= bet:
        if not cmd.bot.cooldown.on_cooldown(cmd.name, message.author):
            cmd.bot.cooldown.set_cooldown(cmd.name, message.author, 60)
            cmd.db.rmv_currency(message.author, bet)
            out_list = []
            for x in range(0, 3):
                temp_list = []
                for y in range(0, 3):
                    rarity = roll_symbol()
                    symbol_choice = symbol_rewards[rarity]
                    temp_list.append(symbol_choice)
                out_list.append(temp_list)
            slot_lines = f'⏸{"".join(out_list[0])}⏸'
            slot_lines += f'\n▶{"".join(out_list[1])}◀'
            slot_lines += f'\n⏸{"".join(out_list[2])}⏸'
            combination = out_list[1]
            if combination[0] == combination[1] == combination[2]:
                win = True
                announce = True
                if combination[0] != '🔥':
                    winnings = int(bet * (rarity_rewards[combination[0]] * 5))
                else:
                    winnings = bet
            elif combination[0] == combination[1] or combination[0] == combination[2] or combination[1] == combination[
                2]:
                if combination[0] == combination[1]:
                    win_comb = combination[0]
                elif combination[0] == combination[2]:
                    win_comb = combination[0]
                elif combination[1] == combination[2]:
                    win_comb = combination[1]
                else:
                    win_comb = None
                win = True
                announce = False
                if win_comb != '🔥':
                    winnings = int(bet * (rarity_rewards[win_comb] * 2))
                else:
                    winnings = bet
            else:
                win = False
                announce = False
                winnings = 0
            if win:
                color = 0x5dadec
                title = '💎 Congrats, you won!'
                footer = f'{currency_icon} {winnings} {currency} has been awarded.'
                cmd.db.add_currency(message.author, message.guild, winnings)
            else:
                color = 0x232323
                title = '💣 Oh my, you lost...'
                footer = f'{currency_icon} {bet} {currency} has been deducted.'
            if announce:
                if 'win_channel' in cmd.cfg:
                    target_channel = discord.utils.find(lambda c: c.id == cmd.cfg['win_channel'],
                                                        cmd.bot.get_all_channels())
                    announce_embed = discord.Embed(color=0xf9f9f9, title=f'🎰 A user just got 3 {combination[0]}.')
                    announce_embed.set_author(name=message.author.display_name, icon_url=user_avatar(message.author))
                    announce_embed.set_footer(text=f'On: {message.guild.name}.', icon_url=message.guild.icon_url)
                    await target_channel.send(embed=announce_embed)
            response = discord.Embed(color=color)
            response.add_field(name=title, value=slot_lines)
            response.set_footer(text=footer)
        else:
            timeout = cmd.bot.cooldown.get_cooldown(cmd.name, message.author)
            response = discord.Embed(color=0x696969, title=f'🕙 You can spin again in {timeout} seconds.')
    else:
        response = discord.Embed(color=0xa7d28b, title=f'💸 You don\'t have enough {currency}.')
    await message.channel.send(embed=response)

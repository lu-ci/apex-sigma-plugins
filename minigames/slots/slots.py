import discord
import secrets
from sigma.core.utilities.data_processing import user_avatar

rarity_rewards = {
    '💎': 20,
    '🔱': 18,
    '💠': 16,
    '🍁': 14,
    '🍆': 12,
    '☀': 10,
    '🍌': 8,
    '☢': 6,
    '☎': 4,
    '🔥': 2
}

symbols = []
for symbol in rarity_rewards:
    symbols.append(symbol)


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
    if bet < 10:
        bet = 10
    if current_kud >= bet:
        if not cmd.bot.cooldown.on_cooldown(cmd.name, message.author):
            cmd.bot.cooldown.set_cooldown(cmd.name, message.author, 60)
            cmd.db.rmv_currency(message.author, bet)
            out_list = []
            for x in range(0, 3):
                temp_list = []
                init_symb = []
                for y in range(0, 3):
                    if not init_symb:
                        symbol_choice = secrets.choice(symbols)
                        init_symb.append(symbol_choice)
                    else:
                        roll = secrets.randbelow(bet + 10)
                        if roll == 0:
                            symbol_choice = secrets.choice(init_symb)
                        else:
                            temp_symb = []
                            for symbol_item in symbols:
                                temp_symb.append(symbol_item)
                            for init_symb_item in init_symb:
                                temp_symb.remove(init_symb_item)
                            symbol_choice = secrets.choice(temp_symb)
                            init_symb.append(symbol_choice)
                    temp_list.append(symbol_choice)
                out_list.append(temp_list)
            slot_lines = f'⏸{"".join(out_list[0])}⏸'
            slot_lines += f'\n▶{"".join(out_list[1])}◀'
            slot_lines += f'\n⏸{"".join(out_list[2])}⏸'
            combination = out_list[1]
            if combination[0] == combination[1] == combination[2]:
                win = True
                announce = True
                winnings = int(bet * (rarity_rewards[combination[0]] * 5))
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
                winnings = int(bet * (rarity_rewards[win_comb] * 2))
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

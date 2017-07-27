import discord
from .nodes.race_storage import *


async def joinrace(cmd, message, args):
    if args:
        try:
            bet_amt = abs(int(args[0]))
        except ValueError:
            bet_amt = 0
    else:
        bet_amt = 0
    if bet_amt:
        kud = cmd.db.get_currency(message.author, message.guild)['current']
        if bet_amt <= kud:
            valid_kud = True
        else:
            valid_kud = False
    else:
        valid_kud = True
    currency = f'{cmd.bot.cfg.pref.currency}'
    if message.channel.id in races:
        if valid_kud:
            race = races[message.channel.id]
            if len(race['users']) < 10:
                user_found = False
                for user in race['users']:
                    if user['user'].id == message.author:
                        user_found = True
                if not user_found:
                    icon = add_participant(message.channel.id, message.author)
                    join_title = f'{icon} {message.author.display_name} joined as a {names[icon]}!'
                    if bet_amt:
                        cmd.db.rmv_currency(message.author, message.guild, bet_amt)
                        join_title += f' And bet {bet_amt} {currency}!'
                        add_to_pool(message.channel.id, bet_amt)
                    response = discord.Embed(color=colors[icon], title=join_title)
                else:
                    response = discord.Embed(color=0xDB0000, title='❗ You already in the race!')
            else:
                response = discord.Embed(color=0xDB0000, title='❗ Sorry, no more room left!')
        else:
            response = discord.Embed(color=0xDB0000, title=f'❗ You don\'t have that much {currency}!')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ There is no ongoing race!')
    await message.channel.send(embed=response)

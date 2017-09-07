import discord
import pymongo
from humanfriendly.tables import format_pretty_table as boop


async def topcookies(cmd, message, args):
    all_cookies = cmd.db[cmd.db.db_cfg.database].Cookies.find({}).sort([{'Cookies', pymongo.DESCENDING}]).limit(20)
    cookie_count = 0
    entire_list = cmd.db[cmd.db.db_cfg.database].Cookies.find({})
    for cookie_big in entire_list:
        cookie_count += cookie_big['Cookies']
    cookie_list = []
    for cookie_file in all_cookies:
        user = discord.utils.find(lambda x: x.id == cookie_file['UserID'], cmd.bot.get_all_members())
        if user:
            unam = user.name
        else:
            unam = '{Unknown}'
        cookie_list.append([unam, cookie_file['Cookies']])
    cookie_table = boop(cookie_list, ['User', 'Cookies'])
    top_text = f'A total of {cookie_count} cookies have been given.'
    response = discord.Embed(color=0xd99e82)
    response.add_field(name='Cookie Count', value=top_text, inline=False)
    response.add_field(name='Cookie Leaderboard', value=f'```bat\n{cookie_table}\n```', inline=False)
    await message.channel.send(embed=response)



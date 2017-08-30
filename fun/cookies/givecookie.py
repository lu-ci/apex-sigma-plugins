import arrow
import discord


async def givecookie(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
        if message.author.id != target.id:
            if not target.bot:
                if not cmd.bot.cooldown.on_cooldown(cmd.name, message.author):
                    cookie_coll = cmd.db[cmd.db.db_cfg.database].Cookies
                    cookie_cd = 3600
                    file_check = cookie_coll.find_one({'UserID': target.id})
                    if not file_check:
                        cookies = 0
                        data = {'UserID': target.id, 'Cookies': 0}
                        cookie_coll.insert_one(data)
                    else:
                        cookies = file_check['Cookies']
                    cookies += 1
                    cookie_coll.update_one({'UserID': target.id}, {'$set': {'Cookies': cookies}})
                    cmd.bot.cooldown.set_cooldown(cmd.name, message.author, cookie_cd)
                    title = f'🍪 You gave a cookie to {target.display_name}.'
                    response = discord.Embed(color=0xd99e82, title=title)
                else:
                    timeout_seconds = cmd.bot.cooldown.get_cooldown(cmd.name, message.author)
                    if timeout_seconds > 60:
                        timeout_seconds = arrow.utcnow().timestamp + timeout_seconds
                        timeout = arrow.get(timeout_seconds).humanize()
                    else:
                        timeout = f'in {timeout_seconds} seconds'
                    timeout_title = f'🕙 You can give another cookie {timeout}.'
                    response = discord.Embed(color=0x696969, title=timeout_title)
            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ Bots don\'t eat cookies.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ Nope, can\'t give cookies to yourself.')
    else:
        response = discord.Embed(color=0xBE1931, title=f'❗ No user targeted.')
    await message.channel.send(embed=response)

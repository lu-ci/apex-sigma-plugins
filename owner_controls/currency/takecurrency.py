import discord


async def takecurrency(cmd, message, args):
    if message.mentions:
        if len(args) >= 2:
            target = message.mentions[0]
            if not target.bot:
                try:
                    amount = abs(int(args[0]))
                    target_amount = cmd.db.get_currency(target, message.guild)['current']
                    if amount <= target_amount:
                        cmd.db.rmv_currency(target, message.guild, amount)
                        title_text = f'🔥 Ok, {amount} of {target.display_name}\'s {cmd.bot.cfg.pref.currency} '
                        title_text += 'has been destroyed.'
                        response = discord.Embed(color=0xFF9900, title=title_text)
                    else:
                        err_title = f'❗ {target.display_name} does\'t have that much {cmd.bot.cfg.pref.currency}.'
                        response = discord.Embed(color=0xDB0000, title=err_title)
                except ValueError:
                    response = discord.Embed(color=0xDB0000, title='❗ Invalid amount.')
            else:
                err_title = f'❗ You can\'t take {cmd.bot.cfg.pref.currency} from bots.'
                response = discord.Embed(color=0xDB0000, title=err_title)
        else:
            response = discord.Embed(color=0xDB0000, title=f'❗ {cmd.bot.cfg.pref.currency} amount and target needed.')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ No user was mentioned.')
    await message.channel.send(embed=response)

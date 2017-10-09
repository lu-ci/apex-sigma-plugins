import discord


async def help(cmd, message, args):
    if args:
        cmd_name = ''.join(args).lower()
        if cmd_name in cmd.bot.modules.alts:
            cmd_name = cmd.bot.modules.alts[cmd_name]
        if cmd_name in cmd.bot.modules.commands:
            command = cmd.bot.modules.commands[cmd_name]
            response = discord.Embed(color=0x1B6F5F, title=f'📄 {command.name.upper()} Usage and Information')
            response.add_field(name='Usage Example', value=f'`{command.usage}`', inline=False)
            response.add_field(name='Command Description', value=f'```\n{command.desc}\n```', inline=False)
            if command.alts:
                response.add_field(name='Command Aliases', value=f'```\n{", ".join(command.alts)}\n```')
        else:
            response = discord.Embed(color=0x696969, title='🔍 No such command was found...')
    else:
        lucia_image = 'https://i.imgur.com/HPuyvT1.png'
        sigma_image = 'https://i.imgur.com/mGyqMe1.png'
        sigma_title = 'Apex Sigma: The Database Giant'
        support_url = 'https://discordapp.com/invite/aEUCHwX'
        response = discord.Embed(color=0x1B6F5F)
        response.set_author(name=sigma_title, icon_url=sigma_image, url=cmd.bot.cfg.pref.website)
        invite_url = f'https://discordapp.com/oauth2/authorize?client_id={cmd.bot.user.id}&scope=bot&permissions=8'
        support_text = f'**Add Me**: [Link]({invite_url})'
        support_text += f' | **Commands**: [Link]({cmd.bot.cfg.pref.website}/commands)'
        support_text += f' | **Server**: [Link]({support_url})'
        response.add_field(name='Help', value=support_text)
        patreon_url = 'https://www.patreon.com/ApexSigma'
        paypal_url = 'https://www.paypal.me/AleksaRadovic'
        donation_text = 'If you could spare some money, it would be amazing of you to support my work. '
        donation_text += 'At the moment support from Sigma\'s users is my only source of income. '
        donation_text += f'Come check out my [Patreon]({patreon_url}) and lend a hand! You also get some goodies! '
        donation_text += f'Or if a subscription is too much commitment for you, how about [PayPal]({paypal_url})?'
        donation_text += f'\n**Thank you to the {len(cmd.bot.info.donors.donors)} donors who have provided support!**'
        response.add_field(name='Care to help out?', value=donation_text)
        response.set_thumbnail(url=sigma_image)
        response.set_footer(text='© by Lucia\'s Cipher. Released under the GPLv3 license.', icon_url=lucia_image)
    await message.channel.send(embed=response)

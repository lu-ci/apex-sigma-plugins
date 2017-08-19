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
        aurora_image = 'https://i.imgur.com/IsUF5x8.png'
        sigma_image = 'https://i.imgur.com/mGyqMe1.png'
        sigma_title = 'Apex Sigma: The Database Giant'
        support_url = 'https://discordapp.com/invite/aEUCHwX'
        response = discord.Embed(color=0x1B6F5F)
        response.set_author(name=sigma_title, icon_url=sigma_image, url=cmd.bot.cfg.pref.website)
        invite_url = f'https://discordapp.com/oauth2/authorize?client_id={cmd.bot.user.id}&scope=bot&permissions=8'
        support_text = f'**Invite**: [Link]({invite_url})'
        support_text += f' | **Website**: [Link]({cmd.bot.cfg.pref.website})'
        support_text += f' | **Support**: [Link]({support_url})'
        response.add_field(name='Help', value=support_text)
        response.set_thumbnail(url=sigma_image)
        response.set_footer(text='© by the Aurora Project. Released under the GPLv3 license.', icon_url=aurora_image)
    await message.channel.send(embed=response)

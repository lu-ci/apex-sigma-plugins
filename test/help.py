import discord
import aiohttp
import json


async def help(cmd, message, args):
    if not args:
        help_json_url = 'https://canary.discordapp.com/api/guilds/200751504175398912/widget.json'
        async with aiohttp.ClientSession() as session:
            async with session.get(help_json_url) as data:
                widget_data = await data.read()
                widget_data = json.loads(widget_data)
                server_invite_url = widget_data['instant_invite']
        help_out = discord.Embed(type='rich', title='❔ Help', color=0x1B6F5F)
        help_out.set_author(name='Apex Sigma', url='http://127.0.0.1',
                            icon_url='https://i.imgur.com/WQbzk9y.png')
        help_out.add_field(name='Website', value=f'[**LINK**]({"http://127.0.0.1"})')
        help_out.add_field(name='Commands', value=f'[**LINK**]({"http://127.0.0.1"}commands)')
        help_out.add_field(name='GitHub', value='[**LINK**](https://github.com/aurora-pro/apex-sigma)')
        help_out.add_field(name='Official Server', value=f'[**LINK**]({server_invite_url})')
        help_out.add_field(name='Add Me',
                           value=f'[**LINK**](https://discordapp.com/oauth2/authorize?client_id={cmd.bot.user.id}&scope=bot&permissions=8)')
        help_out.set_footer(
            text=f'Example: {cmd.bot.cfg.pref.prefix}help greetmsg', icon_url='https://i.imgur.com/f4TyYMr.png')
        help_out.set_image(url='https://i.imgur.com/TRSdGni.png')
    else:
        qry = ' '.join(args).lower()
        if qry in cmd.bot.modules.commands:
            command = cmd.bot.modules.commands[qry]
            help_out = discord.Embed(color=0x1B6F5F, title=f'📖 Command {command.name.upper()} Help')
            help_out.add_field(name='Usage Example', value=f'`{command.usage}`', inline=False)
            help_out.add_field(name='Description', value=f'```\n{command.desc}\n```', inline=False)
        else:
            help_out = discord.Embed(color=0x696969, title=f'🔍 I couldn\'t find {qry} in my commands.')
    await message.channel.send(embed=help_out)

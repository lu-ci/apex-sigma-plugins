import discord


async def byemessage(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_guild:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xDB0000)
    else:
        if args:
            goodbye_text = ' '.join(args)
            cmd.db.set_guild_settings(message.guild.id, 'ByeMessage', goodbye_text)
            response = discord.Embed(title='✅ New Goodbye Message Set', color=0x66CC66)
        else:
            current_goodbye = cmd.db.get_guild_settings(message.guild.id, 'ByeMessage')
            if current_goodbye is None:
                current_goodbye = '{user_name} has left {server_name}.'
            response = discord.Embed(color=0x0099FF)
            response.add_field(name='ℹ Current Goodbye Message', value=f'```\n{current_goodbye}\n```')
    await message.channel.send(embed=response)

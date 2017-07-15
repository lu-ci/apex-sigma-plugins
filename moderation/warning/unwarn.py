import discord


async def unwarn(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_messages:
        response = discord.Embed(title='⛔ Access Denied. Manage Messages needed.', color=0xBE1931)
    else:
        if message.mentions:
            target = message.mentions[0]
            guild_warnings = cmd.db.get_guild_settings(message.guild.id, 'WarnedUsers')
            if guild_warnings is None:
                guild_warnings = {}
            uid = str(target.id)
            if uid in guild_warnings:
                del guild_warnings[uid]
                cmd.db.set_guild_settings(message.guild.id, 'WarnedUsers', guild_warnings)
                response = discord.Embed(color=0x77B255, title=f'✅ {target.name}\'s warnings have been cleared.')
            else:
                response = discord.Embed(color=0x696969, title='🔍 User does not have any warnings.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ No user tagged.')
    await message.channel.send(embed=response)

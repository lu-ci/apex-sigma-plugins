import discord


async def logedits(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_guild:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    else:
        log_edits = cmd.db.get_guild_settings(message.guild.id, 'LogMessageEdits')
        if log_edits:
            cmd.db.set_guild_settings(message.guild.id, 'LogMessageEdits', False)
            ender = 'disabled'
        else:
            cmd.db.set_guild_settings(message.guild.id, 'LogMessageEdits', True)
            ender = 'enabled'
        response = discord.Embed(color=0x77B255, title=f'✅ Message edit logging has been {ender}.')
    await message.channel.send(embed=response)

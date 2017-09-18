import discord


async def logdeletes(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_guild:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xBE1931)
    else:
        log_edits = cmd.db.get_guild_settings(message.guild.id, 'LogMessageDeletes')
        if log_edits:
            cmd.db.set_guild_settings(message.guild.id, 'LogMessageDeletes', False)
            ender = 'disabled'
        else:
            cmd.db.set_guild_settings(message.guild.id, 'LogMessageDeletes', True)
            ender = 'enabled'
        response = discord.Embed(color=0x77B255, title=f'✅ Message deletion logging has been {ender}.')
    await message.channel.send(embed=response)

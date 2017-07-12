import discord


async def prefix(cmd, message, args):
    if message.author.permissions_in(message.channel).manage_guild:
        current_prefix = cmd.bot.get_prefix(message)
        if args:
            new_prefix = ''.join(args)
            if new_prefix != current_prefix:
                cmd.db.set_guild_settings(message.guild.id, 'Prefix', new_prefix)
                response = discord.Embed(color=0x66CC66, title=f'✅ **{new_prefix}** has been set as the new prefix.')
            else:
                response = discord.Embed(color=0xDB0000, title='❗ The current prefix and the new one are the same.')
        else:
            response = discord.Embed(color=0x0099FF, title=f'ℹ **{current_prefix}** is the current prefix.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xDB0000)
    await message.channel.send(embed=response)

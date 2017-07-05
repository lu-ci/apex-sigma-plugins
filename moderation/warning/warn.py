import arrow
import discord


async def warn(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_messages:
        response = discord.Embed(title='⛔ Access Denied. Manage Messages needed.', color=0xDB0000)
    else:
        if message.mentions:
            target = message.mentions[0]
            if len(args) > 1:
                reason = ' '.join(args[1:])
            else:
                reason = 'Reason not provided.'
            guild_warnings = cmd.db.get_guild_settings(message.guild.id, 'WarnedUsers')
            if guild_warnings is None:
                guild_warnings = {}
            uid = str(target.id)
            if uid in guild_warnings:
                warning_list = guild_warnings[uid]
            else:
                warning_list = []
            warning_data = {
                'responsible': {
                    'name': message.author.name,
                    'discriminator': message.author.discriminator,
                    'id': message.author.id
                },
                'reason': reason,
                'timestamp': arrow.utcnow().timestamp
            }
            warning_list.append(warning_data)
            guild_warnings.update({uid: warning_list})
            cmd.db.set_guild_settings(message.guild.id, 'WarnedUsers', guild_warnings)
            response = discord.Embed(color=0x66CC66, title=f'✅ {target.name}#{target.discriminator} has been warned.')
            to_target = discord.Embed(color=0xFF9900)
            to_target.add_field(name='⚠ You received a warning.', value=f'Reason: {reason}')
            to_target.set_footer(text=f'From: {message.guild.name}', icon_url=message.guild.icon_url)
            try:
                await target.send(embed=to_target)
            except discord.Forbidden:
                pass
        else:
            response = discord.Embed(color=0xDB0000, title='❗ No user tagged.')
    await message.channel.send(embed=response)

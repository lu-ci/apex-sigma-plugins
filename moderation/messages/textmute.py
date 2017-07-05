import discord
from sigma.core.utilities.permission_processing import hierarchy_permit


async def textmute(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_messages:
        response = discord.Embed(title='⛔ Access Denied. Manage Messages needed.', color=0xDB0000)
    else:
        if not message.mentions:
            response = discord.Embed(title='❗ No user targeted.', color=0xDB0000)
        else:
            author = message.author
            target = message.mentions[0]
            if author.id == target.id:
                response = discord.Embed(title='❗ Can\'t mute yourself.', color=0xDB0000)
            else:
                above_hier = hierarchy_permit(author, target)
                if not above_hier:
                    response = discord.Embed(title='⛔ Can\'t mute someone equal or above you.', color=0xDB0000)
                else:
                    mute_list = cmd.db.get_guild_settings(message.guild.id, 'MutedUsers')
                    if mute_list is None:
                        mute_list = []
                    if target.id in mute_list:
                        resp_title = f'❗ {target.display_name} is already text muted.'
                        response = discord.Embed(title=resp_title, color=0xDB0000)
                    else:
                        mute_list.append(target.id)
                        cmd.db.set_guild_settings(message.guild.id, 'MutedUsers', mute_list)
                        response = discord.Embed(color=0x66CC66, title=f'✅ {target.display_name} has been text muted.')
                        if len(args) > 1:
                            reason = ' '.join(args[1:])
                            to_target_title = f'⚠ You have been text muted by {author.display_name}'
                            to_target = discord.Embed(color=0xFF9900)
                            to_target.add_field(name=to_target_title, value=f'Reason: {reason}')
                            try:
                                await target.send(embed=to_target)
                            except discord.Forbidden:
                                pass
    await message.channel.send(embed=response)

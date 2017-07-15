import discord
from sigma.core.utilities.permission_processing import hierarchy_permit


async def textunmute(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_messages:
        response = discord.Embed(title='⛔ Access Denied. Manage Messages needed.', color=0xBE1931)
    else:
        if not message.mentions:
            response = discord.Embed(title='❗ No user targeted.', color=0xBE1931)
        else:
            author = message.author
            target = message.mentions[0]
            is_admin = author.permissions_in(message.channel).administrator
            if author.id == target.id and not is_admin:
                response = discord.Embed(title='❗ Can\'t unmute yourself.', color=0xBE1931)
            else:
                above_hier = hierarchy_permit(author, target)
                if not above_hier and not is_admin:
                    response = discord.Embed(title='⛔ Can\'t unmute someone equal or above you.', color=0xBE1931)
                else:
                    mute_list = cmd.db.get_guild_settings(message.guild.id, 'MutedUsers')
                    if mute_list is None:
                        mute_list = []
                    if target.id not in mute_list:
                        resp_title = f'❗ {target.display_name} is not text muted.'
                        response = discord.Embed(title=resp_title, color=0xBE1931)
                    else:
                        mute_list.remove(target.id)
                        cmd.db.set_guild_settings(message.guild.id, 'MutedUsers', mute_list)
                        response = discord.Embed(color=0x77B255, title=f'✅ {target.display_name} has been unmuted.')
    await message.channel.send(embed=response)

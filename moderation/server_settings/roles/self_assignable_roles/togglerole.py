import discord
from sigma.core.utilities.role_processing import matching_role


async def togglerole(cmd, message, args):
    if args:
        lookup = ' '.join(args)
        target_role = matching_role(message.guild, lookup)
        if target_role:
            selfroles = cmd.db.get_guild_settings(message.guild.id, 'SelfRoles')
            if selfroles is None:
                selfroles = []
            if target_role.id in selfroles:
                await message.author.add_roles(target_role, reason='Role self assigned.')
                response = discord.Embed(color=0x77B255, title=f'✅ {target_role.name} has been added to you.')
            else:
                response = discord.Embed(color=0xFF9900, title=f'⚠ {target_role} is not self assignable.')
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 I can\'t find {lookup} on this server.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)

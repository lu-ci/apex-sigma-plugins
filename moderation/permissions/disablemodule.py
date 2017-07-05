import discord
from .nodes.permission_data import get_all_perms


async def disablemodule(cmd, message, args):
    if args:
        if not message.author.permissions_in(message.channel).manage_guild:
            response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xDB0000)
        else:
            mdl_name = args[0].lower()
            if mdl_name in cmd.bot.modules.category_list:
                perms = get_all_perms(cmd.db, message)
                disabled_modules = perms['DisabledModules']
                if mdl_name in disabled_modules:
                    response = discord.Embed(color=0xFF9900, title='⚠ Module Already Disabled')
                else:
                    disabled_modules.append(mdl_name)
                    perms.update({'DisabledModules': disabled_modules})
                    cmd.db[cmd.db.db_cfg.database].Permissions.update_one({'ServerID': message.guild.id}, {'$set': perms})
                    response = discord.Embed(color=0x66CC66, title=f'✅ `{mdl_name.upper()}` disabled.')
            else:
                response = discord.Embed(color=0x696969, title='🔍 Module Not Found')
        await message.channel.send(embed=response)

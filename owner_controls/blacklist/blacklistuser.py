import discord


async def blacklistuser(cmd, message, args):
    if args:
        target_id = ''.join(args)
        try:
            target_id = int(target_id)
            valid_id = True
        except ValueError:
            valid_id = False
        if valid_id:
            target = discord.utils.find(lambda x: x.id == target_id, cmd.bot.get_all_members())
            if target:
                black_user_collection = cmd.db[cmd.bot.cfg.db.database].BlacklistedUsers
                black_user_file = black_user_collection.find_one({'UserID': target.id})
                if black_user_file:
                    cmd.db[cmd.bot.cfg.db.database].BlacklistedUsers.delete_one({'UserID': target.id})
                    result = 'removed from the blacklist'
                    icon = '🔓'
                else:
                    cmd.db[cmd.bot.cfg.db.database].BlacklistedUsers.insert_one({'UserID': target.id})
                    result = 'blacklisted'
                    icon = '🔒'
                title = f'{icon} {target.name}#{target.discriminator} has been {result}.'
                response = discord.Embed(color=0xFFCC4D, title=title)
            else:
                response = discord.Embed(color=0x696969, title='🔍 No user with that ID was found.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid User ID.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ No User ID was inputted.')
    await message.channel.send(embed=response)

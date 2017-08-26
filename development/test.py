import secrets


async def test(cmd, message, args):
    guild_settings = cmd.db.aurora.ServerSettings.find({})
    for gs in guild_settings:
        print(f'Checking guild {gs["ServerID"]}')
        try:
            if 'WarnedUsers' in gs:
                warn_dict = gs['WarnedUsers']
                for uid in warn_dict:
                    warnings = warn_dict[uid]
                    new_warns = []
                    for warning in warnings:
                        if 'id' not in warning:
                            warning.update({'id': secrets.token_hex(2)})
                        new_warns.append(warning)
                    warn_dict.update({uid: new_warns})
                cmd.db.set_guild_settings(gs['ServerID'], 'WarnedUsers', warn_dict)
        except AttributeError:
            cmd.db.set_guild_settings(gs['ServerID'], 'WarnedUsers', {})
    await message.channel.send('All done!')

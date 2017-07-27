import discord

auth_id = 222234484064518156


async def toggledantracker(cmd, message, args):
    if message.author.id == auth_id:
        dbcol = cmd.db[cmd.db.db_cfg.database]['SpecialSettings']
        settings = dbcol.find_one({'Name': 'dan_tracker'})
        if settings:
            active = settings['Value']
        else:
            dbcol.insert_one({'Name': 'dan_tracker'})
            active = True
        if active:
            dbcol.update_one({'Name': 'dan_tracker'}, {'$set': {'Value': False}})
            result = 'deactivated'
        else:
            dbcol.update_one({'Name': 'dan_tracker'}, {'$set': {'Value': True}})
            result = 'activated'
        response = discord.Embed(color=0x66CC66, title=f'✅ Danny tracker {result}.')
    else:
        response = discord.Embed(color=0xDB0000, title='⛔ Access Denied. You are not Nighty nee-chan.')
    await message.channel.send(embed=response)

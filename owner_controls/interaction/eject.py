import discord


async def eject(cmd, message, args):
    if args:
        guild_id = ''.join(args)
        try:
            guild_id = int(guild_id)
            valid_id = True
        except ValueError:
            valid_id = False
        if valid_id:
            target = discord.utils.find(lambda x: x.id == guild_id, cmd.bot.guilds)
            if target:
                await target.leave()
                response = discord.Embed(color=0x66CC66, title=f'✅ Ejected from {target.name}.')
            else:
                response = discord.Embed(color=0x696969, title='🔍 No guild with that ID was found.')
        else:
            response = discord.Embed(color=0xDB0000, title='❗ Invalid Guild ID.')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ No Guild ID was inputted.')
    await message.channel.send(embed=response)

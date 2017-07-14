import discord


async def unban(cmd, message, args):
    if message.author.permissions_in(message.channel).ban_members:
        if args:
            lookup = ' '.join(args)
            target = None
            banlist = await message.guild.bans()
            for entry in banlist:
                if entry.user.name.lower() == lookup.lower():
                    target = entry.user
                    break
            if target:
                await message.guild.unban(target, reason=f'By {message.author.name}.')
                response = discord.Embed(title=f'✅ {target.name} has been unbanned.', color=0x66CC66)
            else:
                response = discord.Embed(title=f'🔍 {lookup} not found in the ban list.')
        else:
            response = discord.Embed(color=0xDB0000, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Ban permissions needed.', color=0xDB0000)
    await message.channel.send(embed=response)

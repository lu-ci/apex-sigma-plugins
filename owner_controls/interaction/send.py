import discord


async def send(cmd, message, args):
    if args:
        mode, identifier = args[0].split(':')
        identifier = int(identifier)
        mode = mode.lower()
        text = ' '.join(args[1:])
        if mode == 'u':
            target = discord.utils.find(lambda x: x.id == identifier, cmd.bot.get_all_members())
            title_end = f'{target.name}#{target.discriminator}'
        elif mode == 's':
            target_srv = discord.utils.find(lambda x: x.id == identifier, cmd.bot.guilds)
            target = target_srv.default_channel
            title_end = f'{target_srv.name}'
        elif mode == 'c':
            target = discord.utils.find(lambda x: x.id == identifier, cmd.bot.get_all_channels())
            title_end = f'#{target.name} on {target.guild.name}'
        else:
            embed = discord.Embed(color=0xDB0000, title='❗ Invalid Arguments Given.')
            await message.channel.send(embed=embed)
            return
        await target.send(text)
        embed = discord.Embed(color=0x66CC66, title=f'✅ Message sent to {title_end}.')
        await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(color=0xDB0000, title='❗ No Arguments Given.')
        await message.channel.send(embed=embed)

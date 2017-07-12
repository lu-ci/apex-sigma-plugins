import discord
from sigma.core.utilities.permission_processing import hierarchy_permit
from sigma.core.utilities.data_processing import user_avatar


async def kick(cmd, message, args):
    if message.author.permissions_in(message.channel).kick_members:
        if message.mentions:
            target = message.mentions[0]
            if cmd.bot.user.id != target.id:
                if message.author.id != target.id:
                    above_hier = hierarchy_permit(message.author, target)
                    is_admin = message.author.permissions_in(message.channel).administrator
                    if above_hier or is_admin:
                        if len(args) > 1:
                            reason = ' '.join(args[1:])
                        else:
                            reason = 'No reason stated.'
                        response = discord.Embed(color=0xc1694f, title=f'👢 The user has been removed.')
                        response_title = f'{target.name}#{target.discriminator}'
                        response.set_author(name=response_title, icon_url=user_avatar(target))
                        to_target = discord.Embed(color=0xc1694f)
                        to_target.add_field(name='👢 You have been kicked.', value=f'Reason: {reason}')
                        to_target.set_footer(text=f'From: {message.guild.name}.', icon_url=message.guild.icon_url)
                        try:
                            await target.send(embed=to_target)
                        except discord.ClientException:
                            pass
                        await target.kick(reason=f'By {message.author.name}: {reason}')
                    else:
                        response = discord.Embed(title='⛔ Can\'t kick someone equal or above you.', color=0xDB0000)
                else:
                    response = discord.Embed(color=0xDB0000, title='❗ You can\'t kick yourself.')
            else:
                response = discord.Embed(color=0xDB0000, title='❗ I can\'t kick myself.')
        else:
            response = discord.Embed(color=0xDB0000, title='❗ No user targeted.')
    else:
        response = discord.Embed(title='⛔ Access Denied. Kick permissions needed.', color=0xDB0000)
    await message.channel.send(embed=response)

import discord


async def warnings(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_messages:
        target = message.author
    else:
        if message.mentions:
            target = message.mentions[0]
        else:
            target = message.author
    guild_warnings = cmd.db.get_guild_settings(message.guild.id, 'WarnedUsers')
    if guild_warnings is None:
        guild_warnings = {}
    uid = str(target.id)
    if uid not in guild_warnings:
        response = discord.Embed(color=0x696969, title='🔍 User does not have any warnings.')
    else:
        warning_list = guild_warnings[uid]
        warning_output = ''
        for warning in warning_list:
            responsible = f'{warning["responsible"]["name"]}#{warning["responsible"]["discriminator"]}'
            warning_output += f'\nFor: "**{warning["reason"]}**"\n- *by {responsible}*.'
        if len(warning_output) > 800:
            warning_output = warning_output[:800] + '\n...'
        warning_title = f'⚠ {target.name} was warned {len(warning_list)} times for...'
        response = discord.Embed(color=0xFFCC4D)
        response.add_field(name=warning_title, value=warning_output, inline=False)
    await message.channel.send(embed=response)

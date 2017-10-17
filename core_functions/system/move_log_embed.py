import arrow


def make_move_log_embed(log_embed, guild):
    gld = guild
    own = guild.owner
    creation_time = arrow.get(gld.created_at).format('DD. MMMM YYYY')
    bot_count = 0
    user_count = 0
    for user in gld.members:
        if user.bot:
            bot_count += 1
        else:
            user_count += 1
    guild_text = f'Name: **{gld.name}**'
    guild_text += f'\nID: **{gld.id}**'
    guild_text += f'\nMembers: **{user_count}**'
    guild_text += f'\nBots: **{bot_count}**'
    guild_text += f'\nChannels: **{len(gld.channels)}**'
    guild_text += f'\nRoles: **{len(gld.roles)}**'
    guild_text += f'\nCreated: **{creation_time}**'
    log_embed.add_field(name='Guild Info', value=guild_text)
    own_creation_time = arrow.get(own.created_at).format('DD. MMMM YYYY')
    own_text = f'Username: **{own.name}**#{own.discriminator}'
    own_text += f'\nNickname: **{own.display_name}**'
    own_text += f'\nID: **{own.id}**'
    own_text += f'\nStatus: **{str(own.status).replace("dnd", "busy").title()}**'
    own_text += f'\nColor: **{str(own.color).upper()}**'
    own_text += f'\nTop Role: **{own.top_role.name}**'
    own_text += f'\nCreated: **{own_creation_time}**'
    log_embed.add_field(name='Owner Info', value=own_text)
    if gld.icon_url:
        log_embed.set_thumbnail(url=gld.icon_url)

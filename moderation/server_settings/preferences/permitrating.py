import discord

text_to_num = {
    'sfw': 0,
    'safe': 0,
    'borderline': 1,
    'explicit': 2
}

num_to_text = {
    '0': 'SFW',
    '1': 'Borderline',
    '2': 'Explicit'
}

icons = {
    0: '🔞',
    1: '🎀',
    2: '🍆'
}

colors = {
    0: 0xf5f8fa,
    1: 0xdd2e44,
    2: 0x744eaa
}


async def permitrating(cmd, message, args):
    if not message.author.permissions_in(message.channel).manage_guild:
        response = discord.Embed(title='⛔ Access Denied. Manage Server needed.', color=0xDB0000)
    else:
        if args:
            new_rating = args[0].lower()
            if new_rating in num_to_text:
                new_rating_number = int(new_rating)
                new_rating_name = num_to_text[new_rating]
            elif new_rating in text_to_num:
                new_rating_number = text_to_num[new_rating]
                new_rating_name = num_to_text[str(text_to_num[new_rating])]
            else:
                new_rating_number = None
                new_rating_name = None
            if new_rating_number is not None and new_rating_name is not None:
                nsfw_collection = cmd.db[cmd.bot.cfg.db.database].NSFWPermissions
                channel_nsfw_file = nsfw_collection.find_one({'channel_id': message.channel.id})
                if channel_nsfw_file:
                    current_ratig_number = channel_nsfw_file['rating']
                else:
                    nsfw_collection.insert_one({'channel_id': message.channel.id, 'rating': 0})
                    current_ratig_number = 0
                current_rating_name = num_to_text[str(current_ratig_number)]
                nsfw_collection.update_one({'channel_id': message.channel.id}, {"$set": {'rating': new_rating_number}})
                change_text = f'from {current_rating_name} to {new_rating_name}'
                embed_title = f'{icons[new_rating_number]} Rating changed {change_text}.'
                response = discord.Embed(color=colors[new_rating_number], title=embed_title)
            else:
                response = discord.Embed(color=0xDB0000, title='❗ Invalid input.')
        else:
            nsfw_collection = cmd.db[cmd.bot.cfg.db.database].NSFWPermissions
            channel_nsfw_file = nsfw_collection.find_one({'channel_id': message.channel.id})
            if channel_nsfw_file:
                current_ratig_number = channel_nsfw_file['rating']
            else:
                current_ratig_number = 0
            current_rating_name = num_to_text[str(current_ratig_number)]
            embed_title = f'{icons[current_ratig_number]} The current allowed rating is {current_rating_name}.'
            response = discord.Embed(color=colors[current_ratig_number], title=embed_title)
    await message.channel.send(embed=response)

import secrets

import discord


async def nablie_plant(ev, message):
    if message.author.id == 211922001546182656:
        roll = secrets.randbelow(5)
        if roll == 0:
            try:
                await message.add_reaction('🍆')
            except discord.Forbidden:
                pass

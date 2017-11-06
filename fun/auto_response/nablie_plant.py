import secrets

import discord

responses = {
    150060705662500864: '🍛',
    211922001546182656: '🍆'
}


async def nablie_plant(ev, message):
    if message.author.id in responses:
        roll = secrets.randbelow(5)
        if roll == 0:
            try:
                await message.add_reaction(responses.get(message.author.id))
            except discord.Forbidden:
                pass

import asyncio
import discord
import random


async def status_rotation(ev):
    if ev.bot.cfg.pref.status_rotation:
        ev.bot.loop.create_task(status_clockwork(ev))


async def status_clockwork(ev):
    while True:
        if ev.bot.cfg.pref.status_rotation:
            statuses = [
                'your mind', 'fire', 'knives', 'some plebs',
                'nuclear launch codes', 'antimatter',
                'chinchillas', 'catgirls', 'foxes',
                'fluffy tails', 'dragon maids', 'traps', 'lovely cakes',
                'tentacle summoning spells', 'genetic engineering',
                'air conditioning', 'anthrax', 'space ninjas',
                'a spicy parfait', 'very nasty things', 'numbers',
                'terminator blueprints', 'love', 'your heart', 'tomatoes',
                'bank accounts', 'your data', 'your girlfriend', 'your boyfriend',
                'Scarlet Johanson', 'a new body', 'cameras', 'NSA\'s documents',
                'mobile suits', 'snakes', 'jelly', 'alcohol', 'the blue king'
            ]
            status = f'with {random.choice(statuses)}'
            game = discord.Game(name=status)
            try:
                await ev.bot.change_presence(game=game)
            except:
                pass
        await asyncio.sleep(60)

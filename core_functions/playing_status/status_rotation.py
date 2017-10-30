import asyncio
import secrets

import discord


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
                'mobile suits', 'snakes', 'jelly', 'alcohol', 'the blue king',
                'political campaigns', 'quartz', 'orbal trinkets', 'tomatoes',
                'the black market', 'Bastion', 'RSA keys', 'md5 hashes',
                'destiny', 'the mentos mafia', 'engine parts', 'steak recipes',
                'scottish whisky', 'my offspring', 'bunnies', 'the occult'
            ]
            status = f'with {secrets.choice(statuses)}'
            game = discord.Game(name=status)
            await ev.bot.change_presence(game=game)
        await asyncio.sleep(180)

import random


async def experience_message(ev, message):
    if not message.author.bot:
        if message.guild:
            prefix = ev.bot.get_prefix(message)
            if not message.content.startswith(prefix):
                if not ev.bot.cooldown.on_cooldown(ev.name, message.author):
                    points = random.randint(3, 9)
                    ev.db.add_experience(message.author, message.guild, points)
                    ev.bot.cooldown.set_cooldown(ev.name, message.author, 60)

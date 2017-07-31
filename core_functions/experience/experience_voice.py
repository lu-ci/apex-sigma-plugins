import asyncio
import secrets


def count_members(guild):
    counter = 0
    for member in guild.members:
        if not member.bot:
            counter += 1
    return counter


def count_vc_members(vc):
    counter = 0
    for member in vc.members:
        if not member.bot:
            if not member.voice.deaf:
                if not member.voice.self_deaf:
                    counter += 1
    return counter


async def experience_voice(ev):
    ev.bot.loop.create_task(clockwork_function_experience_voice(ev))


async def clockwork_function_experience_voice(ev):
    while True:
        members = ev.bot.get_all_members()
        for member in members:
            if not member.bot:
                if member.voice:
                    afk = False
                    if member.guild.afk_channel:
                        afk_id = member.guild.afk_channel.id
                        vc_id = member.voice.channel.id
                        if vc_id == afk_id:
                            afk = True
                    if count_members(member.guild) >= 20:
                        if not afk:
                            if not member.voice.deaf:
                                if not member.voice.self_deaf:
                                    if count_vc_members(member.voice.channel) > 1:
                                        points = 1 + secrets.randbelow(9)
                                        ev.db.add_experience(member, member.guild, points)
        await asyncio.sleep(60)

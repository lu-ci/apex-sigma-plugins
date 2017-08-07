import discord


async def memeify(cmd, message, args):
    if message.mentions:
        usr = message.mentions[0]
    else:
        usr = message.author
    if message.channel_mentions:
        chn = message.channel_mentions[0]
    else:
        chn = message.channel
    unam = usr.name
    dnam = usr.display_name
    cnam = chn.name
    gnam = message.guild.name
    text = f"""
    I miss the old {unam}, straight from the 'Go {unam}
    Chop up the soul {unam}, set on his memes {unam}
    I hate the new {dnam}, the goofy {dnam}
    I miss the sweet {unam}, chop up the memes {unam}
    I gotta to say, at that time I'd like to meet Meme Prime
    See we invented {unam}, born in #{cnam}
    And now i look and look around and there's so many meme primes
    I used to love memes, i used to love {unam}
    What if {unam} made a song, about memes?
    Called "I miss the old {unam}", man that'd be so memetastic
    That's all it was {unam}, we still love {unam}
    And I love you like {gnam} loves {unam} <3
    """
    await message.channel.send(text.replace('  ', ''))

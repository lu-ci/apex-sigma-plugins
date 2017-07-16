import secrets
import discord

answers = [
    'It is certain.',
    'It is decidedly so.',
    'Without a doubt.',
    'Yes. Definitely.',
    'You may rely on it.',
    'I find it highly plausible.',
    'Most likely.',
    'Outlook good.',
    'Yes.',
    'Sings point to yes.',
    'I am a bit hazy, try again later.',
    'I\'m on my coffee break, ask later.',
    'Now is not the time.',
    'I am drawing a blank.',
    'You lack determination, I got nothing.',
    'Don\'t count on it.',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Very doubtful.'
]


async def eightball(cmd, message, args):
    if args:
        answer = secrets.choice(answers)
        response = discord.Embed(color=0x232323, title=f'🎱 {answer}')
    else:
        response = discord.Embed(color=0x696969, title='❔ No question was asked.')
    await message.channel.send(embed=response)

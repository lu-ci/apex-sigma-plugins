import secrets

import discord
import markovify
from cryptography.fernet import Fernet, InvalidToken

titles = {
    'n': 'People can try...',
    'y': 'I flicker back...',
    's': 'Happy thoughts...',
    'm': 'Cacophony of colors...'
}

titles_glitch = {
    'm': 'Flash ng, exp nd ng, piercing...'
}

chars = {
    'n': [
        'https://i.imgur.com/Xr19wxI.png',
        'https://i.imgur.com/RnyKBBn.png'
    ],
    'y': [
        'https://i.imgur.com/isyOw8Y.png',
        'https://i.imgur.com/0bbIGq4.png'
    ],
    's': [
        'https://i.imgur.com/SxnYDHH.png',
        'https://i.imgur.com/cQWGAul.png'
    ],
    'm': [
        'https://i.imgur.com/wJazxfj.png',
        'https://i.imgur.com/6qqfqC7.png'
    ]
}

chars_glitch = {
    'm': 'https://i.imgur.com/im1H8jA.png'
}


def clean(text, author):
    output = text.replace('{i}', '*')
    output = output.replace('{/i}', '*')
    output = output.replace('[player]', author.display_name)
    output = output.replace('[currentuser]', author.name)
    return output


async def dokidoki(cmd, message, args):
    with open('doki/just_monika.luci', 'rb') as quote_file:
        quotes = quote_file.read()
    key = cmd.bot.cfg.pref.raw.get('key_to_my_heart')
    if key:
        key = key.encode('utf-8')
        cipher = Fernet(key)
        try:
            ciphered = cipher.decrypt(quotes).decode('utf-8')
        except InvalidToken:
            ciphered = None
        if ciphered:
            glitch = secrets.randbelow(10)
            glitch = not bool(glitch)
            if glitch:
                line_count = 1
                thumbnail = chars_glitch['m']
            else:
                line_count = 3
                thumbnail = secrets.choice(chars['m'])
            lines = []
            for x in range(0, line_count):
                output = markovify.Text(ciphered).make_short_sentence(500, tries=100)
                output = clean(output, message.author)
                if glitch:
                    output = cipher.encrypt(output.encode('utf-8')).decode('utf-8')
                lines.append(output)
            output_final = ' '.join(lines)
            if glitch:
                title = titles_glitch['m']
            else:
                title = titles['m']
            response = discord.Embed(color=0xe75a70)
            response.add_field(name=f'💟 {title}', value=output_final)
            response.set_thumbnail(url=thumbnail)
        else:
            response = discord.Embed(color=0xe75a70, title='💔 Sorry but that key is incorrect!')
    else:
        response = discord.Embed(color=0xe75a70, title='💔 You are missing the key to my heart!')
    await message.channel.send(embed=response)

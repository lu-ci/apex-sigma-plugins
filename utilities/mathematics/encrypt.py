import discord
from cryptography.fernet import Fernet, InvalidToken, InvalidSignature


async def encrypt(cmd, message, args):
    key = cmd.bot.cfg.pref.raw.get('key_to_my_heart')
    if key:
        if args:
            crypt_text = ' '.join(args).encode('utf-8')
            key = key.encode('utf-8')
            cipher = Fernet(key)
            try:
                ciphered = cipher.encrypt(crypt_text).decode('utf-8')
            except InvalidToken:
                ciphered = None
            except InvalidSignature:
                ciphered = None
            if ciphered:
                response = discord.Embed(color=0xe75a70)
                response.add_field(name=f'💟 Text Encrypted', value=ciphered)
            else:
                response = discord.Embed(color=0xBE1931, title='❗ The token or key are incorrect.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Nothing to decrypt.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You don\'t posses a key.')
    await message.channel.send(embed=response)

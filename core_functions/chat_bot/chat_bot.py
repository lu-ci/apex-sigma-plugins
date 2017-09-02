import json
import aiohttp


async def chat_bot(ev, message):
    active = ev.db.get_guild_settings(message.guild.id, 'ChatterBot')
    if active:
        mention = f'<@{ev.bot.user.id}>'
        mention_alt = f'<@!{ev.bot.user.id}>'
        if message.content.startswith(mention) or message.content.startswith(mention_alt):
            args = message.content.split(' ')
            interaction = ' '.join(args[1:])
            if message.mentions:
                for mnt in message.mentions:
                    interaction = interaction.replace(mnt.mention, mnt.name)
            bot_url = f'http://www.zabaware.com/webhal/chat.asp?q={interaction}'
            async with aiohttp.ClientSession() as session:
                async with session.get(bot_url) as data:
                    data = await data.read()
            chat_data = None
            tries = 0
            while not chat_data and tries < 3:
                try:
                    chat_data = json.loads(data)
                except Exception:
                    tries += 1
            if chat_data:
                bot_response = chat_data['HalResponse'].replace('Hal', 'Sigma')
            else:
                bot_response = 'Sorry, I am not feeling very well at the moment...'
            response = f'{message.author.mention} {bot_response}'
            await message.channel.send(response)

import json
import aiohttp
import discord


async def urbandictionary(cmd, message, args):
    if 'api_key' in cmd.cfg:
        api_key = cmd.cfg['api_key']
        if args:
            ud_input = ' '.join(args)
            url = "https://mashape-community-urban-dictionary.p.mashape.com/define?term=" + ud_input
            headers = {'X-Mashape-Key': api_key, 'Accept': 'text/plain'}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as data_response:
                    data = await data_response.read()
                    data = json.loads(data)
            result_type = str((data['result_type']))
            if result_type == 'exact':
                definition = str((data['list'][0]['definition']))
                if len(definition) > 750:
                    definition = definition[:750] + '...'
                example = str((data['list'][0]['example']))
                response = discord.Embed(color=0xe27e00, title=f'🥃 Urban Dictionary: `{ud_input.upper()}`')
                response.add_field(name='Definition', value=definition)
                response.add_field(name='Usage Example', value=example)
            else:
                response = discord.Embed(color=0x696969, title='🔍 Unable to find exact results.')
        else:
            response = discord.Embed(color=0xDB0000, title='❗ Nothing inputted.')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ The API Key is missing.')
    await message.channel.send(None, embed=response)

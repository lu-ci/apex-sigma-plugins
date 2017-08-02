import discord
from .nodes.item_core import ItemCore

item_core = None

async def finditem(cmd, message, args):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    if args:
        if len(args) >= 2:
            item_type = args[0].lower()
            lookup = ' '.join(args[1:])
            try:
                inv = item_core.all_items[item_type]
            except KeyError:
                inv = None
            if inv:
                item = item_core.get_item_by_name(lookup)
                if item:
                    connector = 'A'
                    if item.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                        connector = 'An'
                    item_info = f'{connector} **{item.rarity_name.title()} {item.type.title()}**'
                    item_info += f'\nIt is valued at **{item.value} {cmd.bot.cfg.pref.currency}**'
                    response = discord.Embed(color=item.color)
                    response.add_field(name=f'{item.icon} {item.name}', value=f'{item_info}')
                    response.add_field(name='Item Description', value=f'{item.desc}', inline=False)
                else:
                    response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find any {lookup} in your inventory.')
            else:
                response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find the {item_type} category.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Not enough arguments..')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You didn\'t input anything.')
    await message.channel.send(embed=response)

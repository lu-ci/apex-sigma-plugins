import discord
from .nodes.item_core import ItemCore

item_core = None

async def inspect(cmd, message, args):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    if args:
        inv = cmd.db.get_inventory(message.author)
        if inv:
            lookup = ' '.join(args)
            item_o = item_core.get_item_by_name(lookup)
            if item_o:
                item = cmd.db.get_inventory_item(message.author, item_o.file_id)
            else:
                item = None
            if item:
                connector = 'A'
                if item_o.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                    connector = 'An'
                item_info = f'{connector} **{item_o.rarity_name.title()} {item_o.type.title()}**'
                item_info += f'\nIt is valued at **{item_o.value} {cmd.bot.cfg.pref.currency}**'
                response = discord.Embed(color=item_o.color)
                response.add_field(name=f'{item_o.icon} {item_o.name}', value=f'{item_info}')
                response.add_field(name='Item Description', value=f'{item_o.desc}', inline=False)
                response.set_footer(text=f'ItemID: {item["item_id"]}')
            else:
                response = discord.Embed(color=0x696969, title=f'🔍 I didn\'t find any {lookup} in your inventory.')
        else:
            response = discord.Embed(color=0xc6e4b5, title=f'💸 Your inventory is empty, {message.author.name}...')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ You didn\'t input anything.')
    await message.channel.send(embed=response)

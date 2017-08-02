import discord
from .nodes.item_core import ItemCore

item_core = None


async def filtersell(cmd, message, args):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    if args:
        full_qry = ' '.join(args)
        arguments = full_qry.split(':')
        if len(arguments) >= 2:
            mode = arguments[0].lower()
            lookup = ' '.join(arguments[1:])
            inv = cmd.db.get_inventory(message.author)
            if inv:
                sell_count = 0
                sell_value = 0
                if mode == 'name':
                    attribute = 'name'
                elif mode == 'type':
                    attribute = 'item_type'
                elif mode == 'rarity' or mode == 'quality':
                    attribute = 'rarity_name'
                else:
                    attribute = None
                if attribute:
                    for item in inv:
                        item_ob_id = item_core.get_item_by_file_id(item['item_file_id'])
                        item_attribute = getattr(item_ob_id, attribute)
                        if item_attribute.lower() == lookup.lower():
                            sell_value += item_ob_id.value
                            sell_count += 1
                            cmd.db.del_from_inventory(message.author, item['item_id'])
                    cmd.db.add_currency(message.author, message.guild, sell_value)
                    currency = cmd.bot.cfg.pref.currency
                    sell_title = f'💶 You sold {sell_count} items for {sell_value} {currency}.'
                    response = discord.Embed(color=0xc6e4b5, title=sell_title)
                else:
                    response = discord.Embed(color=0xBE1931, title='❗ Invalid arguments.')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Your inventory is empty.')
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Invalid number of arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)

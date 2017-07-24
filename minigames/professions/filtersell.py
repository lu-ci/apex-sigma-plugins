import discord
from .mechanics import get_item_by_id, get_all_items
from .mechanics import items


async def filtersell(cmd, message, args):
    if not items:
        get_all_items('fish', cmd.resource('data'))
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
                        item_ob_id = get_item_by_id(item['item_file_id'])
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
                    response = discord.Embed(color=0xDB0000, title='❗ Invalid arguments.')
            else:
                response = discord.Embed(color=0xDB0000, title='❗ Your inventory is empty.')
        else:
            response = discord.Embed(color=0xDB0000, title='❗ Invalid number of arguments.')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ Nothing inputted.')
    await message.channel.send(embed=response)

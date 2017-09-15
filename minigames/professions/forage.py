import discord
from .nodes.item_core import ItemCore
from sigma.core.utilities.data_processing import user_avatar

item_core = None


async def forage(cmd, message, args):
    global item_core
    if not item_core:
        item_core = ItemCore(cmd.resource('data'))
    if not cmd.bot.cooldown.on_cooldown(cmd.name, message.author):
        inv = cmd.db.get_inventory(message.author)
        inv_limit = 64
        if len(inv) < inv_limit:
            cmd.bot.cooldown.set_cooldown(cmd.name, message.author, 60)
            rarity = item_core.roll_rarity()
            if args:
                if message.author.id in cmd.bot.cfg.dsc.owners:
                    try:
                        rarity = int(args[0])
                    except TypeError:
                        pass
            item = item_core.pick_item_in_rarity('plants', rarity)
            value = item.value
            connector = 'a'
            if item.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                connector = 'an'
            if value == 0:
                if item.name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                    connector = 'an'
                response_title = f'{item.icon} You found {connector} {item.name} and threw it away!'
            else:
                response_title = f'{item.icon} You found {connector} {item.rarity_name} {item.name}!'
                data_for_inv = item.generate_inventory_item()
                cmd.db.add_to_inventory(message.author, data_for_inv)
            response = discord.Embed(color=item.color, title=response_title)
            response.set_author(name=message.author.display_name, icon_url=user_avatar(message.author))
            if item.rarity >= 5:
                if 'item_channel' in cmd.cfg:
                    await item_core.notify_channel_of_special(message, cmd.bot.get_all_channels(),
                                                              cmd.cfg['item_channel'], item)

        else:
            response = discord.Embed(color=0xBE1931,
                                     title=f'❗ Your inventory is full with {len(inv)}/{inv_limit}.')
    else:
        timeout = cmd.bot.cooldown.get_cooldown(cmd.name, message.author)
        response = discord.Embed(color=0x696969, title=f'🕙 You are resting for another {timeout} seconds.')
    await message.channel.send(embed=response)

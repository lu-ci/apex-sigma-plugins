import os
import yaml
import secrets
import discord
from .properties import *
from .item_object import SigmaItem
from sigma.core.utilities.data_processing import user_avatar


class ItemCore(object):
    def __init__(self, item_directory):
        self.base_dir = item_directory
        self.item_types = item_types
        self.rarity_names = rarity_names
        self.item_icons = item_icons
        self.item_colors = item_colors
        self.all_items = {}
        self.init_items()

    def get_item_by_name(self, name):
        output = None
        for category in self.all_items:
            item_list = self.all_items[category]
            for item in item_list:
                if item.name.lower() == name.lower():
                    output = item
                    break
        return output

    def get_item_by_file_id(self, name):
        output = None
        for category in self.all_items:
            item_list = self.all_items[category]
            for item in item_list:
                if item.file_id == name:
                    output = item
                    break
        return output

    def pick_item_in_rarity(self, item_category, rarity):
        items = self.all_items[item_category]
        in_rarity = []
        for item in items:
            if item.rarity == rarity:
                in_rarity.append(item)
        choice = secrets.choice(items)
        return choice

    def init_items(self):
        for list_item in self.item_types:
            output = []
            for root, dirs, files in os.walk(f'{self.base_dir}/{list_item.lower()}'):
                for file in files:
                    if file.endswith('.yml'):
                        file_path = (os.path.join(root, file))
                        with open(file_path) as item_file:
                            item_id = file.split('.')[0]
                            item_data = yaml.safe_load(item_file)
                            item_data.update({'file_id': item_id})
                            item_object = SigmaItem(item_data)
                            output.append(item_object)
            self.all_items.update({list_item: output})

    @staticmethod
    def roll_rarity():
        rarities = {
            0: 0,
            1: 35000,
            2: 60000,
            3: 80000,
            4: 95000,
            5: 98000,
            6: 99100,
            7: 99600,
            8: 99850,
            9: 99950
        }
        roll = secrets.randbelow(100000)
        lowest = 0
        for rarity in rarities:
            if rarities[rarity] <= roll:
                lowest = rarity
            else:
                break
        return lowest

    @staticmethod
    async def notify_channel_of_special(message, all_channels, channel_id, item):
        if channel_id:
            target = discord.utils.find(lambda x: x.id == channel_id, all_channels)
            if target:
                connector = 'a'
                if item.rarity_name[0].lower() in ['a', 'e', 'i', 'o', 'u']:
                    connector = 'an'
                response_title = f'{item.icon} {connector.title()} {item.rarity_name} {item.name} has been found!'
                response = discord.Embed(color=item.color, title=response_title)
                response.set_author(name=f'{message.author.display_name}', icon_url=user_avatar(message.author))
                response.set_footer(text=f'From {message.guild.name}.', icon_url=message.guild.icon_url)
                await target.send(embed=response)

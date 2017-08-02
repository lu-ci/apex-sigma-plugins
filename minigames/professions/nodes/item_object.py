import secrets
from .properties import *


class SigmaItem(object):
    def __init__(self, item_data):
        self.name = item_data['name']
        self.desc = item_data['description']
        self.rarity = item_data['rarity']
        self.type = item_data['type']
        self.rarity_name = rarity_names[self.rarity]
        self.icon = item_icons[self.type.lower()][self.rarity]
        self.color = item_colors[self.type.lower()][self.rarity]
        self.value = item_data['value']
        self.file_id = item_data['file_id']

    def generate_inventory_item(self):
        token = secrets.token_hex(16)
        data = {
            'item_id': token,
            'item_file_id': self.file_id
        }
        return data

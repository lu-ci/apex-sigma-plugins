import discord
import secrets
from .nodes.recipe_core import RecipeCore
from humanfriendly.tables import format_pretty_table as boop

recipe_core = None


async def recipes(cmd, message, args):
    global recipe_core
    if not recipe_core:
        recipe_core = RecipeCore(cmd.resource('data'))
    if args:
        try:
            page = int(args[0]) - 1
            if page < 0:
                page = 0
        except ValueError:
            page = 0
    else:
        page = 0
    list_start = page * 10
    list_end = (page + 1) * 10
    recipe_list = sorted(recipe_core.recipes, key=lambda x: x.name)[list_start:list_end]
    recipe_look = secrets.choice(recipe_core.recipes)
    recipe_icon = recipe_look.icon
    recipe_color = recipe_look.color
    recipe_boop_head = ['Name', 'Type', 'Value']
    recipe_boop_list = []
    stats_text = f'Showing recipes: {list_start}-{list_end}.'
    stats_text += f'\nThere is a total of {len(recipe_core.recipes)} recipes.'
    if recipe_list:
        for recipe in recipe_list:
            recipe_boop_list.append([recipe.name, recipe.type, recipe.value])
        recipe_table = boop(recipe_boop_list, recipe_boop_head)
        response = discord.Embed(color=recipe_color)
        response.add_field(name=f'{recipe_icon} Recipe Stats', value=f'```py\n{stats_text}\n```', inline=False)
        response.add_field(name=f'📰 Recipes On Page {page + 1}', value=f'```hs\n{recipe_table}\n```')
    else:
        response = discord.Embed(color=0x696969, title=f'🔍 This page is empty.')
    await message.channel.send(embed=response)

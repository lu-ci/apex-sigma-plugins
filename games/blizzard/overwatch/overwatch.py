import discord
from overwatch_api.core import AsyncOWAPI

ow_cli = AsyncOWAPI(request_timeout=30)
ow_icon = 'https://i.imgur.com/YZ4w2ey.png'
region_convert = {
    'europe': 'eu',
    'korea': 'kr',
    'na': 'us',
    'americas': 'us',
    'america': 'us',
    'china': 'cn',
    'japan': 'jp'
}


async def overwatch(cmd, message, args):
    init_resp = discord.Embed(color=0xff9c00)
    init_resp.set_author(name='Processing information...', icon_url=ow_icon)
    init_resp_msg = await message.channel.send(embed=init_resp)
    if args:
        if len(args) >= 2:
            region = args[0].lower()
            if region in region_convert:
                region = region_convert[region]
            region_list = ['eu', 'kr', 'us', 'cn', 'jp']
            if region in region_list:
                battletag = ' '.join(args[1:])
                profile = await ow_cli.get_profile(battletag, regions=region)
                if profile:
                    profile = profile[region]
                    stats = profile['stats']['quickplay']
                    profile_url = f'https://playoverwatch.com/en-us/career/pc/{region}/{battletag.replace("#", "-")}'
                    gen = stats['overall_stats']
                    if gen['prestige']:
                        gen_section = f'Level: {(gen["prestige"] * 100) + gen["level"]}'
                    else:
                        gen_section = f'Level: {gen["level"]}'
                    gen_section += f'\nGames: {gen["games"]}'
                    gen_section += f'\nWon: {gen["wins"]}'
                    gen_section += f'\nLost: {gen["losses"]}'
                    gen_section += f'\nRank: {gen["comprank"]}'
                    gms = stats['game_stats']
                    gms_section = f'Eliminations: {gms["eliminations"]}'
                    gms_section += f'\nBest Kill Streak: {gms["kill_streak_best"]}'
                    if 'melee_final_blows' in gms:
                        gms_section += f'\nMelee Final Blows: {gms["melee_final_blows"]}'
                    else:
                        gms_section += f'\nMelee Final Blows: None'
                    gms_section += f'\nBest Multikill: {gms["multikill_best"]}'
                    gms_section += f'\nDamage Done: {gms["all_damage_done"]}'
                    gms_section += f'\nDeaths: {gms["deaths"]}'
                    gms_section += f'\nMedals Collected: {gms["medals"]}'
                    response = discord.Embed(color=0xff9c00)
                    response.set_author(name=battletag, icon_url=gen["avatar"], url=profile_url)
                    response.add_field(name='Profile Info', value=gen_section)
                    response.add_field(name='Total Stats', value=gms_section)
                    footer_text = 'Click the battletag at the top to see the user\'s profile.'
                    response.set_footer(text=footer_text, icon_url=ow_icon)
                else:
                    response = discord.Embed(color=0x696969, title='🔍 No results.')
            else:
                region_error_text = f'Supported: {", ".join(region_list)}.\nOr: {", ".join(list(region_convert))}.'
                response = discord.Embed(color=0xBE1931)
                response.add_field(name='❗ Invalid region.', value=region_error_text)
        else:
            response = discord.Embed(color=0xBE1931, title='❗ Region and Battletag needed.')
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    await init_resp_msg.edit(embed=response)

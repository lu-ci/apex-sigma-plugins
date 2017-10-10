import ftfy
import discord
import markovify
import functools
from concurrent.futures import ThreadPoolExecutor
from sigma.core.utilities.data_processing import user_avatar


threads = ThreadPoolExecutor(max_workers=2)


async def impersonate(cmd, message, args):
    if message.mentions:
        target = message.mentions[0]
    else:
        if args:
            target = discord.utils.find(lambda x: x.name.lower() == ' '.join(args).lower(), message.guild.members)
        else:
            target = message.author
    if target:
        init_embed = discord.Embed(color=0xbdddf4, title='💭 Hmm... Let me think...')
        init_message = await message.channel.send(embed=init_embed)
        chain_data = cmd.db[cmd.db.db_cfg.database]['MarkovChains'].find_one({'UserID': target.id})
        if chain_data:
            total_string = ' '.join(chain_data['Chain'])
            total_string = ftfy.fix_text(total_string)
            chain = await cmd.bot.loop.run_in_executor(threads, functools.partial(markovify.Text, total_string))
            chain_function = functools.partial(chain.make_short_sentence, max_chars=150)
            task = cmd.bot.loop.run_in_executor(threads, chain_function)
            sentence = await task
            if not sentence:
                response = discord.Embed(color=0xBE1931, title='😖 I could not think of anything...')
            else:
                sentence = ftfy.fix_text(sentence)
                response = discord.Embed(color=0xbdddf4)
                response.set_author(name=target.name, icon_url=user_avatar(target))
                response.add_field(name='💭 Hmm... something like...', value=sentence)
                pat_url = 'https://www.patreon.com/ApexSigma'
                pat_img = 'https://i.imgur.com/86UvnRv.png'
                response.set_footer(icon_url=pat_img, text=f'Support Sigma! {pat_url}')
        else:
            response = discord.Embed(color=0x696969)
            prefix = cmd.bot.get_prefix(message)
            title = f'🔍 Chain Data Not Found For {target.name}'
            value = f'You can make one with `{prefix}collectchain @{target.name} #channel`!'
            response.add_field(name=title, value=value)
        await init_message.edit(embed=response)

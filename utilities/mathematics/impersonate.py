from sigma.core.utilities.data_processing import user_avatar
import markovify
import discord
import ftfy


async def impersonate(cmd, message, args):
        if message.mentions:
            target = message.mentions[0]
        else:
            if args:
                target = discord.utils.find(lambda x: x.name.lower() == ' '.join(args).lower(), message.guild.members)
            else:
                target = message.author
        if target:
            chain_data = cmd.db[cmd.db.db_cfg.database]['MarkovChains'].find_one({'UserID': target.id})
            if chain_data:
                total_string = ' '.join(chain_data['Chain'])
                total_string = ftfy.fix_text(total_string)
                chain = markovify.Text(total_string)
                sentence = chain.make_sentence(tries=100)
                if not sentence:
                    response = discord.Embed(color=0xDB0000, title='😖 I Couldn\'t think of anything...')
                else:
                    sentence = ftfy.fix_text(sentence)
                    response = discord.Embed(color=0xbdddf4)
                    response.set_author(name=target.name, icon_url=user_avatar(target))
                    response.add_field(name='💭 Hmm... something like...', value=f'```\n{sentence}\n```')
            else:
                response = discord.Embed(color=0x696969)
                prefix = cmd.bot.get_prefix(message)
                title = f'🔍 Chain Data Not Found For {target.name}'
                value = f'You can make one with `{prefix}collectchain @{target.name} #channel`!'
                response.add_field(name=title, value=value)
            await message.channel.send(None, embed=response)

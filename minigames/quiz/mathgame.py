import discord
import secrets
import asyncio

ongoing_list = []


async def mathgame(cmd, message, args):
    if message.channel.id not in ongoing_list:
        ongoing_list.append(message.channel.id)
        if args:
            try:
                diff = int(args[0])
                if diff < 1:
                    diff = 1
                elif diff > 9:
                    diff = 9
            except ValueError:
                diff = 1
        else:
            diff = 1
        max_num = diff * 25
        kud_reward = int(diff * 1.9) + secrets.randbelow(5)
        math_operators = ['*', '/', '+', '-']
        problem_string = str(secrets.randbelow(max_num))
        for x in range(0, diff):
            num = secrets.randbelow(max_num)
            problem_string += f' {secrets.choice(math_operators)} {num}'
        result = round(eval(problem_string), 2)
        question_embed = discord.Embed(color=0x3B88C3, title=f'#⃣ {problem_string} = ?')
        await message.channel.send(embed=question_embed)

        def check_answer(msg):
            if message.channel.id == msg.channel.id:
                try:
                    an_num = int(msg.content)
                    if an_num == result:
                        correct = True
                    else:
                        correct = False
                except ValueError:
                    correct = False
            else:
                correct = False
            return correct

        try:
            answer_message = await cmd.bot.wait_for('message', check=check_answer, timeout=30)
            cmd.db.add_currency(answer_message.author, message.guild, kud_reward)
            author = answer_message.author.display_name
            currency = cmd.bot.cfg.pref.currency
            win_title = f'🎉 Correct, {author}, it was {result}. You won {kud_reward} {currency}!'
            win_embed = discord.Embed(color=0x77B255, title=win_title)
            await message.channel.send(embed=win_embed)
        except asyncio.TimeoutError:
            timeout_title = f'🕙 Time\'s up! It was {result}...'
            timeout_embed = discord.Embed(color=0x696969, title=timeout_title)
            await message.channel.send(embed=timeout_embed)
        ongoing_list.remove(message.channel.id)
    else:
        ongoing_error = discord.Embed(color=0xBE1931, title='❗ There is one already ongoing.')
        await message.channel.send(embed=ongoing_error)

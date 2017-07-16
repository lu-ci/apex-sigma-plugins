import arrow
import discord
import hashlib
from sigma.core.utilities.data_processing import user_avatar


def convert_to_seconds(time_input):
    indent_list = time_input.split(':')
    if len(indent_list) == 3:
        output = (3600 * int(indent_list[0])) + (60 * int(indent_list[1]) + int(indent_list[2]))
    elif len(indent_list) == 2:
        output = (60 * int(indent_list[0]) + int(indent_list[1]))
    elif len(indent_list) == 1:
        output = int(indent_list[0])
    else:
        raise LookupError
    return output


async def remind(cmd, message, args):
    if args:
        time_req = args[0]
        try:
            in_seconds = convert_to_seconds(time_req)
            if len(args) > 1:
                text_message = ' '.join(args[1:])
            else:
                text_message = 'No reminder message set.'
            execution_stamp = arrow.utcnow().timestamp + in_seconds
            timestamp = arrow.get(execution_stamp).datetime
            if in_seconds < 60:
                time_diff = f'In {in_seconds} seconds'
            else:
                time_diff = arrow.get(execution_stamp).humanize(arrow.utcnow())
            crypt = hashlib.new('md5')
            crypt.update(f'{message.id}+{execution_stamp}'.encode('utf-8'))
            final = crypt.hexdigest()
            reminder_data = {
                'ReminderID': final,
                'UserID': message.author.id,
                'CreationStamp': arrow.utcnow().timestamp,
                'ExecutionStamp': execution_stamp,
                'ChannelID': message.channel.id,
                'ServerID': message.guild.id,
                'TextMessage': text_message
            }
            cmd.db[cmd.db.db_cfg.database]['Reminders'].insert_one(reminder_data)
            response = discord.Embed(color=0x66CC66, timestamp=timestamp)
            response.set_author(name='New Reminder Set', icon_url=user_avatar(message.author))
            response.add_field(name='🕑 Until Reminder', value=time_diff.title(), inline=False)
            response.add_field(name='🗒 Reminder Message', value=text_message, inline=False)
        except LookupError:
            response = discord.Embed(color=0xDB0000, title='❗ Please use the format HH:MM:SS.')
        except ValueError:
            response = discord.Embed(color=0xDB0000, title='❗ Inputted value is invalid.')
    else:
        response = discord.Embed(color=0xDB0000, title='❗ No arguments inputted.')
    await message.channel.send(embed=response)

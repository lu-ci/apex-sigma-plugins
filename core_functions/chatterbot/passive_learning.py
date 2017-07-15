from sigma.plugins.core_functions.chatterbot.nodes.cb_instance_storage import get_cb

temp_msg_storage = {}


def check_for_bot_prefixes(pfx, text):
    common_pfx = [pfx, '!', '/', '\\', '~', '.', '>', '-', '_']
    prefixed = False
    for pfx in common_pfx:
        if text.startswith(pfx):
            prefixed = True
            break
    return prefixed


def check_applicable_content(ev, message):
    applicable = False
    if message.content:
        if message.content != '':
            if len(message.content) > 3:
                pfx = ev.bot.get_prefix(message)
                if not check_for_bot_prefixes(pfx, message.content):
                    if 'http' not in message.content and '```' not in message.content:
                        if len(message.content) <= 256:
                            applicable = True
    return applicable


def clean_content(message):
    content = message.content
    if message.mentions:
        for mention in message.mentions:
            content = content.replace(mention.mention, mention.name)
    if message.channel_mentions:
        for mention in message.channel_mentions:
            content = content.replace(mention.mention, mention.name)
    unallowed_chars = ['`', '\n', '\\', '\\n']
    for char in unallowed_chars:
        content = content.replace(char, '')
    if not content.endswith(('.' or '?' or '!')):
        content += '.'
    return content


async def passive_learning(ev, message):
    if message.guild:
        db_cfg = ev.bot.cfg.db
        cb = get_cb(db_cfg)
        applicable = check_applicable_content(ev, message)
        if applicable:
            content = clean_content(message)
            cid = message.channel.id
            uid = message.author.id
            if cid in temp_msg_storage:
                data = temp_msg_storage[cid]
                if data:
                    if uid == data['uid']:
                        data.update({'text': (data['text'] + f' {content}')})
                    else:
                        response_list = [data['text'], content]
                        cb.train(response_list)
                        del temp_msg_storage[cid]
                else:
                    del temp_msg_storage[cid]
            else:
                data = {
                    'uid': uid,
                    'text': content
                }
                temp_msg_storage.update({cid: data})

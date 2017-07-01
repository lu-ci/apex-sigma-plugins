from sigma.plugins.core_functions.chatterbot.nodes.cb_instance_storage import get_cb


def check_for_bot_prefixes(pfx, text):
    common_pfx = [pfx, '!', '/', '\\', '~', '.', '>', '-', '_']
    prefixed = False
    for pfx in common_pfx:
        if text.startswith(pfx):
            prefixed = True
            break
    return prefixed


async def passive_learning(ev, message):
    db_cfg = ev.bot.cfg.db
    cb = get_cb(db_cfg)
    if message.content:
        if message.content != '':
            if len(message.content) > 3:
                pfx = ev.bot.get_prefix(message)
                if not check_for_bot_prefixes(pfx, message.content):
                    if 'http' not in message.content and '```' not in message.content:
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
                        if len(content) >= 5:
                            if not content.endswith(('.' or '?' or '!')):
                                content += '.'
                            cb.get_response(content)

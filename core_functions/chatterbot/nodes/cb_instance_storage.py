from chatterbot import ChatBot

cb = None


def get_cb(db_cfg):
    global cb
    if not cb:
        if db_cfg.auth:
            db_address = f'mongodb://{db_cfg.username}:{db_cfg.password}'
            db_address += f'@{db_cfg.host}:{db_cfg.port}/'
        else:
            db_address = f'mongodb://{db_cfg.host}:{db_cfg.port}/'
        cb = ChatBot(
            'Sigma',
            storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
            database='chatterbot',
            database_uri=db_address,
            output_adapter='chatterbot.output.OutputAdapter',
            output_format='text',
            read_only=False
        )
    return cb

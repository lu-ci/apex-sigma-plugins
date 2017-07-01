from chatterbot.trainers import ChatterBotCorpusTrainer

from sigma.plugins.core_functions.chatterbot.nodes.cb_instance_storage import get_cb


async def startup_check(ev):
    db_cfg = ev.bot.cfg.db
    found = ev.db['chatterbot'].statements.find_one({})
    if not found:
        ev.log.info('Chatterbot data not found, training...')
        cb = get_cb(db_cfg)
        cb.set_trainer(ChatterBotCorpusTrainer)
        cb.train('chatterbot.corpus.english')
        ev.log.info('Chatterbot English corpus training completed!')

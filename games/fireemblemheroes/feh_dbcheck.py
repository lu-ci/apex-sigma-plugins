import pymongo
from sigma.plugins.games.fireemblemheroes.feh_scrapwiki import scrap_all, insert_into_db
from sigma.core.mechanics.config import Configuration


# Set up external DB connection
db_cfg = Configuration().db_cfg_data
if db_cfg['auth']:
    db_address = f"mongodb://{db_cfg['username']}:{db_cfg['password']}"
    db_address += f"@{db_cfg['host']}:{db_cfg['port']}/"
else:
    db_address = f"mongodb://{db_cfg['host']}:{db_cfg['port']}/"

# Iterate through data in the database and build an index for fuzzy searching
db = pymongo.MongoClient(db_address)
db = db.get_database(db_cfg['database']).get_collection('FEHData')


async def feh_dbcheck(event):
    if not db.count():
        data = await scrap_all()
        insert_into_db(data)

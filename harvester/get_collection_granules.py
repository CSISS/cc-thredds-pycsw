import sys
assert sys.version_info >= (3,6)

from lib.indexdb import IndexDB

import json

if len(sys.argv) != 4:
    print("Usage:   get_collection_granules.py collection-catalog-xml-url start-time end-time")
    exit(1)

_, collection_url, start, end = sys.argv


db = IndexDB(config['index_db_url'])

granules = db.get_granules(collection_url, start, end)

print(json.dumps(granules))


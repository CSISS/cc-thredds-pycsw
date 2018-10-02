import sys
assert sys.version_info >= (3,6)

from lib.indexdb import IndexDB
from lib.config import config
from lib.timestamp_util import timestamp_parser

import json

if len(sys.argv) != 4:
    print("Usage:   get_collection_granules.py collection-catalog-xml-url start-time end-time")
    exit(1)

_, collection_url, start, end = sys.argv

start = timestamp_parser.parse_datetime(start)
end = timestamp_parser.parse_datetime(end)

db = IndexDB(config['index_db_url'])

granules = db.get_collection_granules(collection_url, start, end)

for g in granules:
    g['time_start'] = timestamp_parser.to_str(g['time_start'])
    g['time_end'] = timestamp_parser.to_str(g['time_end'])

print(json.dumps(granules))


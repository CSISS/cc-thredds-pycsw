import sys
assert sys.version_info >= (3,6)

from lib.threaded_harvester import ThreadedHarvester
from lib.collection_granule_indexer import CollectionGranuleIndexer

from lib.siphon.catalog import TDSCatalog, Dataset

from lib.indexdb import IndexDB
from lib.config import config

import datetime

def is_index_expired(db, url):
    margin = datetime.timedelta(minutes = 10)
    cutoff = datetime.datetime.now() - margin

    index_datetime = db.get_collection_updated_at(url)
    if index_datetime and index_datetime > cutoff:
        print("index NOT EXPIRED")
        return False
    
    print("index EXPIRED")
    return True




if len(sys.argv) != 3:
    print("Usage:   index_collection_granules.py collection-catalog-xml-url collection-name")
    exit(1)

_, collection_catalog_url, collection_name = sys.argv

print("INDEX: %s %s" % (collection_catalog_url, collection_name))


db = IndexDB(config['index_db_url'])

if not is_index_expired(db, collection_catalog_url):
    print("Recent index available for %s. Doing nothing" %  collection_catalog_url)
    exit(0)


indexer = CollectionGranuleIndexer()

harvester = ThreadedHarvester(indexer, 40, 10)

catalog = TDSCatalog(collection_catalog_url)

harvester.harvest(catalog.catalog_refs.values())

results = indexer.indexes

print("discovered %d granules" % len(results))



db.index_collection_granules(collection_name, collection_catalog_url, results)


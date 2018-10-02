import sys
assert sys.version_info >= (3,6)

from lib.threaded_harvester import ThreadedHarvester
from lib.collection_granule_indexer import CollectionGranuleIndexer

from lib.siphon.catalog import TDSCatalog, Dataset

from lib.indexdb import IndexDB

from lib.config import config


if len(sys.argv) != 3:
    print("Usage:   index_collection_granules.py collection-catalog-xml-url collection-name")
    exit(1)

_, collection_catalog_url, collection_name = sys.argv

indexer = CollectionGranuleIndexer()

harvester = ThreadedHarvester(indexer, 1, 10)

catalog = TDSCatalog(collection_catalog_url)

harvester.harvest(catalog.catalog_refs.values())

results = indexer.indexes



db = IndexDB(config['index_db_url'])

db.index_granules(collection_name, collection_catalog_url, results)


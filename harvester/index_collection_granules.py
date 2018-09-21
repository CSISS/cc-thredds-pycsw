import sys
assert sys.version_info >= (3,6)

from lib.threaded_harvester import ThreadedHarvester
from lib.collection_granule_indexer import CollectionGranuleIndexer

from lib.siphon.catalog import TDSCatalog, Dataset



# take ARGV of collection xml url and collection name
# writes to database a list of tuples
# (collection_name, granule_id, start_time, end_time)
# that's it for now - nothing more, nothing less
# later feel free to add logic to populate CSW or whatevs
# add fancier architecture to allow distributed throughput or whatever, microservices, whatever
# simple process call right now

if len(sys.argv) != 3:
    print("Usage:   index_collection_granules.py collection-catalog-xml-url collection-name")
    exit(1)

_, collection_catalog_url, collection_name = sys.argv

indexer = CollectionGranuleIndexer()

harvester = ThreadedHarvester(indexer, 1, 10)

catalog = TDSCatalog(collection_catalog_url)

harvester.harvest(catalog.catalog_refs.values())

results = indexer.indexes

print(results)



# write results to SQL database here
# write_to_sql(indexer.results, collection_catalog_url, collection_name)

import sys
assert sys.version_info >= (3,6)




from lib.collection_scraper import CollectionScraper
from lib.harvester import Harvester

from siphon.catalog import TDSCatalog, Dataset



scraper = CollectionScraper(Queue(maxsize=0))

harvester = Harvester(scraper, num_workers=1, queue_timeout=10)

catalog = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml')

harvester.harvest(catalog.catalog_refs.values())

import sys
assert sys.version_info >= (3,6)


from lib.threaded_harvester import ThreadedHarvester
from lib.collection_scraper import CollectionScraper

from lib.siphon.catalog import TDSCatalog, Dataset


scraper = CollectionScraper()

harvester = ThreadedHarvester(scraper, 40, 10)

catalog = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml')

harvester.harvest(catalog.catalog_refs.values())

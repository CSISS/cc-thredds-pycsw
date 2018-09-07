import sys
assert sys.version_info >= (3,6)


from lib.harvester import Harvester
from lib.collection_scraper import CollectionScraper

from siphon.catalog import TDSCatalog, Dataset


scraper = CollectionScraper()

harvester = Harvester(scraper, 1, 10)

catalog = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml')

harvester.harvest(catalog.catalog_refs.values())

import sys
assert sys.version_info >= (3,6)


from lib.threaded_harvester import ThreadedHarvester
from lib.collection_scraper import CollectionScraper

from lib.siphon.catalog import TDSCatalog, Dataset


scraper = CollectionScraper()

harvester = ThreadedHarvester(scraper, 40, 10)

top_cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml')


# some sample collections
refs = {}
refs['forecast'] = top_cat.catalog_refs['Forecast Model Data']
refs['satellite infrared'] = top_cat.catalog_refs['Satellite Data'].follow().catalog_refs['Infrared (11 um)']

refs['nexrad2-tjua'] = top_cat.catalog_refs['Radar Data'].follow() \
            .catalog_refs['NEXRAD Level II Radar WSR-88D']

# refs['nexrad3-pta-yux'] = top_cat.catalog_refs['Radar Data'].follow() \
#             .catalog_refs['NEXRAD Level III Radar'].follow()\
#             .catalog_refs['PTA']


# harvester.harvest(top_cat.catalog_refs.values())

harvester.harvest(refs.values())

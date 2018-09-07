import sys
assert sys.version_info >= (3,6)


from lib.harvester import Harvester
from lib.granule_scraper import GranuleScraper

from siphon.catalog import TDSCatalog, Dataset


scraper = GranuleScraper()

harvester = Harvester(scraper, 1, 10)

top_cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml')

# some sample granules
refs = {}
refs['forecast'] = top_cat.catalog_refs['Forecast Model Data']
refs['satellite infrared'] = top_cat.catalog_refs['Satellite Data'].follow().catalog_refs['Infrared (11 um)']

refs['nexrad2-tjua'] = top_cat.catalog_refs['Radar Data'].follow() \
            .catalog_refs['NEXRAD Level II Radar WSR-88D'].follow() \
            .catalog_refs['TJUA']

refs['nexrad3-pta-yux'] = top_cat.catalog_refs['Radar Data'].follow() \
            .catalog_refs['NEXRAD Level III Radar'].follow()\
            .catalog_refs['PTA'].follow() \
            .catalog_refs['YUX']


harvester.harvest(refs.values())

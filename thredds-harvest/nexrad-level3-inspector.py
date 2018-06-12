# create a CSV file containing list of tuples (variable, site, numdays)

from siphon.catalog import TDSCatalog
from siphon.catalog import Dataset

import lib.siphon_ext

cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml').follow_refs('Radar Data', 'NEXRAD Level III Radar')


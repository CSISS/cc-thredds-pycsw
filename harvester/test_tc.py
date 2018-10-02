from lib.siphon.catalog import TDSCatalog, Dataset
# tc = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml')
# c1 = tc.follow_refs('Radar Data', 'NEXRAD Level III Radar', 'PTA', 'YUX', '20180930')
# c2 = TDSCatalog('http://thredds.ucar.edu/thredds/catalog/satellite/IR/WEST-CONUS_4km/20180920/catalog.xml')
# c3 = TDSCatalog('http://thredds.ucar.edu/thredds/catalog/grib/NCEP/GEFS/Global_1p0deg_Ensemble/members-analysis/GEFS_Global_1p0deg_Ensemble_ana_20180930_0000.grib2/catalog.xml')
# print(cat.datasets[0].time_coverage)

from lib.indexdb import IndexDB

# print(IndexDB.create_sql_tables())

# pgcli -h localhost -p 8432 pycsw postgres
# CREATE DATABASE thredds_granule_index
db = IndexDB('postgresql://postgres:mypass@localhost:8432/thredds_granule_index')
# db = IndexDB('postgresql://postgres:mypass@localhost:8432/pycsw')
# rows = db.query('SELECT datname FROM pg_database')

# db.drop_sql_tables()
# db.create_sql_tables()



from datetime import datetime, timedelta

delta = timedelta(minutes=10)

s1 = datetime.now()
e1 = s1 + delta

s2 = e1 + timedelta(hours=1)
e2 = s2 + delta

granules = []
granules.append(('granule1', 'http://thredd.ucar.edu/catalogs/col1/iso/granule1.xml', s1, e1))
granules.append(('granule2', 'http://thredd.ucar.edu/catalogs/col1/iso/granule2.xml', s2, e2))

db.index_granules('COL1', 'http://thredd.ucar.edu/catalogs/col1.xml', granules)

# print(rows.all())
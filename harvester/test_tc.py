from lib.siphon.catalog import TDSCatalog, Dataset
# tc = TDSCatalog('http://thredds.ucar.edu/thredds/catalog.xml')
# c3 = tc.follow_refs('Radar Data', 'NEXRAD Level III Radar', 'PTA', 'YUX', '20180918')
# c3 = tc.follow_refs('Radar Data', 'NEXRAD Level III Radar', 'PTA', 'YUX', '20180918')
# cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog/satellite/IR/WEST-CONUS_4km/20180920/catalog.xml')
cat = TDSCatalog('http://thredds.ucar.edu/thredds/catalog/grib/NCEP/GEFS/Global_1p0deg_Ensemble/members-analysis/GEFS_Global_1p0deg_Ensemble_ana_20180910_0000.grib2/catalog.xml')
print(cat.datasets[0].time_coverage)

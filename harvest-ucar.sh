#!/bin/bash

set -x

curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/idd/forecastModels.xml"

curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/idd/forecastProdsAndAna.xml"

curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/idd/obsData.xml"

curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/idd/satellite.xml"


# RADARS
curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/catalog/nexrad/level3/catalog.xml"

curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/catalog/terminal/level3/catalog.xml"

curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/catalog/nexrad/level2/catalog.xml"

curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/catalog/nexrad/composite/gini/catalog.xml"

curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/catalog/grib/nexrad/composite/unidata/catalog.xml"

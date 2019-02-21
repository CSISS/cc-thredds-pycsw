#!/bin/bash

set -x

curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/idd/forecastModels.xml"

curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/idd/forecastProdsAndAna.xml"

curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/idd/obsData.xml"

curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/idd/radars.xml"

curl http://localhost:8002/index -X POST -d "catalog_url=http://thredds.ucar.edu/thredds/idd/satellite.xml"


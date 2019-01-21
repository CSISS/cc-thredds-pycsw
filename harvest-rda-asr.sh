#!/bin/bash

set -x

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.1/asr15.anl.2D/catalog.xml"

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.1/asr15.anl.3D/catalog.xml"

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.1/asr15.anl.monthly/catalog.xml"

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.1/asr15.fcst3.2D/catalog.xml"

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.1/asr15.fcst3.3D/catalog.xml"

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.1/asr15.fcst3.monthly/catalog.xml"

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.1/invariant/catalog.xml"
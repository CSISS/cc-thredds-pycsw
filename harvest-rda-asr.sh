#!/bin/bash

set -x

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.0/asr30fnl.anl.2D/catalog.xml"

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.0/asr30fnl.anl.3D/catalog.xml"

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.0/asr30fnl.anl.monthly/catalog.xml"

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.0/asr30fnl.fcst3.2D/catalog.xml"

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.0/asr30fnl.fcst3.3D/catalog.xml"

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.0/asr30fnl.fcst3.monthly/catalog.xml"

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.0/asr30km.invariant/catalog.xml"

curl http://localhost:8002/harvest/granules -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.0/asrfinal30km.invariant/catalog.xml"

#!/bin/bash

set -x

curl http://localhost:8002/index -X POST -d "catalog_url=https://rda.ucar.edu/thredds/catalog/files/g/ds631.1/catalog.xml"


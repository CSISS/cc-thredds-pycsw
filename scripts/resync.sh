#!/bin/bash

docker-compose -f docker/docker-compose.yml up -d


# harvest and generate
cd /opt/cc-thredds-pycsw/thredds-harvest

./md_remove_expired.sh
python3 md_harvest.py
python3 md_generate.py


# import into pycsw
cd /opt/cc-thredds-pycsw/docker-compose-pycsw

./records-import.sh

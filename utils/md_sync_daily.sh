#!/bin/bash

# clear old files
cd /opt/cc-thredds-pycsw
scripts/md_remove_expired.sh

# harvest and generate
cd /opt/cc-thredds-pycsw/harvester
python3 harvest_granules.py
python3 harvest_collections.py


# import into pycsw
cd /opt/cc-thredds-pycsw
scripts/records-clear.sh
scripts/records-import.sh
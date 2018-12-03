#!/bin/bash

# harvest and generate
cd /opt/cc-thredds-pycsw/harvester

#./md_remove_expired.sh
python3 harvest_granules.py
python3 harvest_collections.py


# import into pycsw
cd /opt/cc-thredds-pycsw
script/records-clear.sh
script/records-import.sh
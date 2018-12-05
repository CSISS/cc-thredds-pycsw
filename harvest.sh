#!/bin/sh
set -x

## HARVESTER

# tell harvester_indexer to harvest
curl http://localhost:8001/harvest/granules -X POST
curl http://localhost:8001/harvest/collection -X POST


### PYCSW

# delete old records files
docker exec -ti pycsw  find /records -mtime +17 -type f -delete

# delete old records from pycsw
docker exec -ti pycsw  pycsw-admin.py -c delete_records -f /etc/pycsw/pycsw.cfg -y

# import granule records
docker exec -ti pycsw  pycsw-admin.py -c load_records -f /etc/pycsw/pycsw.cfg -p /records/granules -r -y

# import collections records
docker exec -ti pycsw  pycsw-admin.py -c load_records -f /etc/pycsw/pycsw.cfg -p /records/collections -r -y




#!/bin/bash
set -x
sudo chown -R 1000:1000 records
sudo chmod -R a+rw records

#echo clear records
docker exec -ti pycsw  pycsw-admin.py -c delete_records -f /etc/pycsw/pycsw.cfg -y

# echo import granule records
docker exec -ti pycsw  pycsw-admin.py -c load_records -f /etc/pycsw/pycsw.cfg -p /records/granules -r -y

#echo import collections records
docker exec -ti pycsw  pycsw-admin.py -c load_records -f /etc/pycsw/pycsw.cfg -p /records/collections -r -y



#!/bin/bash
set -x
sudo chown -R 1000:1000 ../records

echo clear records
docker exec -ti pycsw  pycsw-admin.py -c delete_records -f /etc/pycsw/pycsw.cfg -y

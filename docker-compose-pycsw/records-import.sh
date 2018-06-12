#!/bin/bash
chown -R 1000:1000 records

echo clear records
docker exec -ti docker-compose-pycsw_db_1  pycsw-admin.py -c delete_records -f /etc/pycsw/pycsw.cfg -y

echo import 
docker exec -ti docker-compose-pycsw_db_1  pycsw-admin.py -c load_records -f /etc/pycsw/pycsw.cfg -p /records -r -y


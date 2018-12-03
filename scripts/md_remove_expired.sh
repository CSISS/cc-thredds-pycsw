#!/bin/bash

# delete all generated
# rm -rf /opt/cc-thredds-pycsw/records/generated/*

# delete older than 17 days
# find /opt/cc-thredds-pycsw/records/harvested -mtime +17 -type f -delete

sudo chown -R 1000:1000 /opt/cc-thredds-pycsw/records
find /opt/cc-thredds-pycsw/records -type f -delete


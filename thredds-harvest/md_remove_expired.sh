#!/bin/bash

# delete all generated
rm -rf /opt/cc-thredds-pycsw/records/generated/*

# delete older than 17 days
find /opt/cc-thredds-pycsw/records/harvested -mtime +17 -type f -delete

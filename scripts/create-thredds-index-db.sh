#!/bin/bash

#docker exec -u pycsw -ti pycsw /bin/ash
docker exec -u postgres -ti db createdb thredds_granule_index

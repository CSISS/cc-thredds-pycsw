#!/bin/sh
#clear the invalid unidata records in CSW cron job
#author Z.S. (zsun@gmu.edu) June 14 2017

DATE=`date +%Y%m%d`

REDLINEDATE=$(($DATE-20))

echo "The red-line date is:"$REDLINEDATE

echo "Start sweeping.."

java -jar /home/geo2015/GitHub/CyberConnector/current/build/threddsharvest-runnable.jar -c http://cube.csiss.gmu.edu/srv/csw -t http://thredds.ucar.edu/thredds/catalog.xml -m sweep -u $REDLINEDATE >/opt/pycsw/sweep.$DATE.log

echo "Sweeping is over. Leaving.."


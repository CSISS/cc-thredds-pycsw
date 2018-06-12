#!/bin/sh
#harvest unidata cron job
#author Z.S. (zsun@gmu.edu) June 14 2017

DATE=`date +%Y%m%d`

LASTDATE=$(($DATE-3))

echo "Today is "$DATE". Last update date is "$LASTDATE". Begin to harvest Unidata."

echo "java -jar /home/geo2015/GitHub/CyberConnector/current/build/threddsharvest-runnable.jar -c http://cube.csiss.gmu.edu/srv/csw -t http://thredds.ucar.edu/thredds/idd/forecastModels.xml -m update -u "$LASTDATE" -i /opt/pycsw/idx/forecastmodels."$DATE".idx >/opt/pycsw/log/forecastmodels."$DATE".log"

java -jar /home/geo2015/GitHub/CyberConnector/current/build/threddsharvest-runnable.jar -c http://cube.csiss.gmu.edu/srv/csw -t http://thredds.ucar.edu/thredds/idd/forecastModels.xml -m update -u $LASTDATE -i "/opt/pycsw/idx/forecastmodels."$DATE".idx" >/opt/pycsw/log/forecastmodels.$DATE.log

echo "java -jar /home/geo2015/GitHub/CyberConnector/current/build/threddsharvest-runnable.jar -c http://cube.csiss.gmu.edu/srv/csw -t http://thredds.ucar.edu/thredds/idd/forecastProdsAndAna.xml -m update -u "$LASTDATE" -i /opt/pycsw/idx/forecastProdsAndAna."$DATE".idx >/opt/pycsw/log/forecastProdsAndAna."$DATE".log"

java -jar /home/geo2015/GitHub/CyberConnector/current/build/threddsharvest-runnable.jar -c http://cube.csiss.gmu.edu/srv/csw -t http://thredds.ucar.edu/thredds/idd/forecastProdsAndAna.xml -m update -u $LASTDATE -i "/opt/pycsw/idx/forecastProdsAndAna."$DATE".idx" >/opt/pycsw/log/forecastProdsAndAna.$DATE.log

echo "java -jar /home/geo2015/GitHub/CyberConnector/current/build/threddsharvest-runnable.jar -c http://cube.csiss.gmu.edu/srv/csw -t http://thredds.ucar.edu/thredds/idd/obsData.xml -m update -u "$LASTDATE" -i /opt/pycsw/idx/obsData."$DATE".idx >/opt/pycsw/log/obsData."$DATE".log"

java -jar /home/geo2015/GitHub/CyberConnector/current/build/threddsharvest-runnable.jar -c http://cube.csiss.gmu.edu/srv/csw -t http://thredds.ucar.edu/thredds/idd/obsData.xml -m update -u $LASTDATE -i "/opt/pycsw/idx/obsData."$DATE".idx" >/opt/pycsw/log/obsData.$DATE.log

echo "java -jar /home/geo2015/GitHub/CyberConnector/current/build/threddsharvest-runnable.jar -c http://cube.csiss.gmu.edu/srv/csw -t http://thredds.ucar.edu/thredds/idd/satellite.xml -m update -u "$LASTDATE" -i /opt/pycsw/idx/satellite."$DATE".idx >/opt/pycsw/log/satellite."$DATE".log"

java -jar /home/geo2015/GitHub/CyberConnector/current/build/threddsharvest-runnable.jar -c http://cube.csiss.gmu.edu/srv/csw -t http://thredds.ucar.edu/thredds/idd/satellite.xml -m update -u $LASTDATE -i "/opt/pycsw/idx/satellite."$DATE".idx" >/opt/pycsw/log/satellite.$DATE.log

echo "Registration is over. Leaving.."


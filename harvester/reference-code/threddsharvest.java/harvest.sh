#!/bin/bash
rm -rf threddsharvest/out/*
javac -d threddsharvest/out/ -cp 'threddsharvest/lib/*' threddsharvest/src/edu/gmu/csiss/*.java



build index: -t http://thredds.ucar.edu/thredds/idd/forecastModels.xml -m init -ro true -i forecastModels.idx  -c http://cube.csiss.gmu.edu/srv/csw 
crawl index into csw: -t http://thredds.ucar.edu/thredds/idd/forecastModels.xml -m init -co -i forecastModels.idx
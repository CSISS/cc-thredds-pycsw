## Clone git repo
```
cd /opt
git clone https://github.com/CSISS/cc-thredds-pycsw.git
chmod a+r /opt/cc-thredds-pycsw/docker-compose-pycsw/pycsw.cfg
```

## Initialize records folder

```
cd /opt/cc-thredds-pycsw
mkdir records
mkdir records/harvested
mkdir records/generated
```


## Start pycsw with upstart

```
cp /opt/cc-thredds-pycsw/upstart/pycsw.conf /etc/init/
mkdir -p /opt/cc-thredds-pycsw/tmp

start pycsw
```


## Fix docker-compose zlib issue (on some systems)

__https://github.com/docker/compose/issues/1339__

If you see this issue:

`docker-compose: error while loading shared libraries: libz.so.1: failed to map segment from shared object: Operation not permitted`


Run:

```
mkdir -p /opt/cc-thredds-pycsw/tmp
export TMPDIR=/opt/cc-thredds-pycsw/tmp
```

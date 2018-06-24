## Initialize records folder
mkdir records

mkdir records/harvested

mkdir records/generated


## Fix docker-compose zlib issue (on some systems)

`docker-compose: error while loading shared libraries: libz.so.1: failed to map segment from shared object: Operation not permitted`
`https://github.com/docker/compose/issues/1339`

`export TMPDIR=/opt/cc-pycsw/tmp`

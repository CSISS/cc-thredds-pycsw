#!/bin/bash

function timeout() { perl -e 'alarm shift; exec @ARGV' "$@"; }


retry() {
    local -r -i max_attempts="$1"; shift
    local -r cmd="$@"
    local -i attempt_num=1

    until $cmd
    do
        if (( attempt_num == max_attempts ))
        then
            echo "Attempt $attempt_num failed and there are no more attempts left!"
            return 1
        else
            echo "Attempt $attempt_num failed! Trying again in $attempt_num seconds..."
            sleep $(( attempt_num++ ))
        fi
    done
}


timed_curl_wait() {
	local -i timeout="$1"
	local -r url="$2"

	echo "Waiting $timeout seconds for $url to respond with \"done\""

	until [[ $timeout -le 0 ]]; do
		local response=$(curl --silent "$url")

		if [[ $response == '"done"' ]]; then
			return 0
			echo
			echo "curl $url done succesfully"
		else
			# not done. wait longer
			sleep 5
			echo -n "."
			let timeout=timeout-5
		fi
	done

	# timed out
	echo
	echo "curl $url timed out"
	return 1
}

# set -x



# ## HARVESTER

# tell harvester_indexer to harvest
curl http://localhost:8001/harvest/granules -X POST
timed_curl_wait 600 "http://localhost:8001/harvest/granules"


curl http://localhost:8001/harvest/collections -X POST
timed_curl_wait 600 "http://localhost:8001/harvest/collections"


# ### PYCSW

# # delete old records files
# docker exec -ti pycsw  find /records -mtime +17 -type f -delete

# # delete old records from pycsw
# docker exec -ti pycsw  pycsw-admin.py -c delete_records -f /etc/pycsw/pycsw.cfg -y

# # import granule records
# docker exec -ti pycsw  pycsw-admin.py -c load_records -f /etc/pycsw/pycsw.cfg -p /records/granules -r -y

# # import collections records
# docker exec -ti pycsw  pycsw-admin.py -c load_records -f /etc/pycsw/pycsw.cfg -p /records/collections -r -y




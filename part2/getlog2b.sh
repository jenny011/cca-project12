# !/bin/bash

CURR=$PWD
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env2.sh

if [ $# != 2 ] || [[ $1 != "1" && $1 != "3" && $1 != "6" && $1 != "12" ]] || [[ ! $2 =~ ^[0-9]+$ ]] || (($2 > 5))
then
	echo "Usage: ./run2b.sh <thd number> <workload number>"
	echo "Thd number:"
	echo "- 1"
	echo "- 3"
	echo "- 6"
	echo "- 12"
	echo "Workload number:"
	echo "- 0: dedup"
	echo "- 1: blackscholes"
	echo "- 2: ferret"
	echo "- 3: freqmine"
	echo "- 4: canneal"
	echo "- 5: fft"
	exit 1
fi
	

# workload
NAME=("dedup" "blackscholes" "ferret" "freqmine" "canneal" "splash2x-fft")
WORKLOAD="parsec-${NAME[$(($2))]}"

echo "> thread num: $1	> workload num: $2"
echo "get log: $WORKLOAD"
kubectl logs $(kubectl get pods --selector=job-name=$WORKLOAD --output=jsonpath='{.items[*].metadata.name}') > $DATADIR/part2b-data/$1/$2.dat

echo "Kill the jobs with ./kill2.sh before starting a new experiment"
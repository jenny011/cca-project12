# !/bin/bash

CURR=$PWD
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env2.sh

if [ $# != 2 ] || [[ ! $1 =~ ^[0-9]+$ ]] || (($1 > 6)) || [[ ! $2 =~ ^[0-9]+$ ]] || (($2 > 5))
then
	echo "Usage: ./get-output.sh <interference number> <workload number>"
	echo "Interference number:"
	echo "- 0: no"
	echo "- 1: cpu"
	echo "- 2: l1d"
	echo "- 3: l1i"
	echo "- 4: l2"
	echo "- 5: llc"
	echo "- 6: membw"
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

echo "> interference num: $1	> workload num: $2"
echo "get log: $WORKLOAD"
kubectl logs $(kubectl get pods --selector=job-name=$WORKLOAD --output=jsonpath='{.items[*].metadata.name}') > $DATADIR/part2a-data/$1/$2.dat

echo "Kill the jobs with ./kill2.sh before starting a new experiment"
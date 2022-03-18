# !/bin/bash

CURR=$PWD
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env1.sh
cd $PART1_YAML_PATH
echo ">>>>> You are in $PART1_YAML_PATH >>>>>"

if [ $# != 1 ] || [ $1 -eq 0 ] || [[ ! $1 =~ ^[0-9]+$ ]] || (($1 > 6))
then
	echo "Usage: ./kill1.sh <a number>"
	echo "Valid numbers:"
	echo "- 1: ibench-cpu"
	echo "- 2: ibench-l1d"
	echo "- 3: ibench-l1i"
	echo "- 4: ibench-l2"
	echo "- 5: ibench-llc"
	echo "- 6: ibench-membw"
	exit 1
fi

NAME=("cpu" "l1d" "l1i" "l2" "llc" "membw")
BENCHMARK="ibench-${NAME[$(($1 - 1))]}"
echo "Killing job $BENCHMARK"
# Kill the experiment
kubectl delete pods $BENCHMARK
if [ $? -ne 0 ]; then
	echo "ERROR: delete pod $BENCHMARK failed."
	exit 1
fi

echo "!!!!! MUST delete the cluster after use: run delete_cluster.sh !!!!!"
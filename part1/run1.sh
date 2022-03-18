# !/bin/bash

CURR=$PWD
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env1.sh
cd $PART1_YAML_PATH
echo ">>>>> You are in $PART1_YAML_PATH >>>>>"

if [ $# != 1 ] || [[ ! $1 =~ ^[0-9]+$ ]] || (($1 > 6))
then
	echo "Usage: ./run1.sh <a number>"
	echo "Valid numbers:"
	echo "- 0: No interference"
	echo "- 1: ibench-cpu"
	echo "- 2: ibench-l1d"
	echo "- 3: ibench-l1i"
	echo "- 4: ibench-l2"
	echo "- 5: ibench-llc"
	echo "- 6: ibench-membw"
	exit 1
fi

if [ $1 -eq "0" ]; then
	# Measure 0. no interference
	# Output pods info to a file
	kubectl get pods -o wide > $PODS
	if [ $? -ne 0 ]; then
		echo "run 'kubectl get pods -o wide > <your-path-to-pods-output-file>' manually in the terminal"
		echo "ERROR: get pods info failed."
		exit 1
	fi
	echo "--------"
	cat $NODES
	echo "--------"
	cat $PODS
	echo "--------"
	# [In nodes] run exp
else 
	# Measure 1-6. ibench-<name>
	NAME=("cpu" "l1d" "l1i" "l2" "llc" "membw")
	BENCHMARK="ibench-${NAME[$(($1 - 1))]}"
	echo "You are setting up $BENCHMARK"
	kubectl create -f interference/$BENCHMARK.yaml
	if [ $? -ne 0 ]; then
		echo "ERROR: interference/$BENCHMARK.yaml create failed."
		exit 1
	fi

	sleep 60
	# if READY is not 1/1 and STATUS is not Running, manually run get pods again
	kubectl get pods -o wide > $PODS
	if [ $? -ne 0 ]; then
		echo "ERROR: get pods info failed."
		echo "run 'kubectl get pods -o wide > <your-path-to-pods-output-file>' manually in the terminal"
		exit 1
	fi
	echo "--------"
	cat $NODES
	echo "--------"
	cat $PODS
	echo "--------"
fi

# [In nodes] run exp
# Kill the measurement job
# run ./stop1.sh

echo "!!!!! MUST delete the cluster after use: run delete_cluster.sh !!!!!"

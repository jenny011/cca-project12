# !/bin/bash

CURR=$PWD
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env2.sh
cd $PART2_YAML_PATH
echo ">>>>> You are in $PART2_YAML_PATH >>>>>"

if [ $# != 2 ] || [[ ! $1 =~ ^[0-9]+$ ]] || (($1 > 6)) || [[ ! $2 =~ ^[0-9]+$ ]] || (($2 > 5))
then
	echo "Usage: ./run2a.sh <interference number> <workload number>"
	echo "Interference number:"
	echo "- 0: No interference"
	echo "- 1: ibench-cpu"
	echo "- 2: ibench-l1d"
	echo "- 3: ibench-l1i"
	echo "- 4: ibench-l2"
	echo "- 5: ibench-llc"
	echo "- 6: ibench-membw"
	echo "Workload number:"
	echo "- 0: dedup"
	echo "- 1: blackscholes"
	echo "- 2: ferret"
	echo "- 3: freqmine"
	echo "- 4: canneal"
	echo "- 5: fft"
	exit 1
fi

if [ $1 -ne "0" ]; then
	# Measure 1-6. ibench-<name>
	NAME=("cpu" "l1d" "l1i" "l2" "llc" "membw")
	BENCHMARK="ibench-${NAME[$(($1 - 1))]}"
	echo "You are setting up interference-parsec/$BENCHMARK.yaml"
	kubectl create -f interference-parsec/$BENCHMARK.yaml
	if [ $? -ne 0 ]; then
		echo "ERROR: interference-parsec/$BENCHMARK.yaml create failed."
		exit 1
	fi

	sleep 10
fi 
	
# if READY is not 1/1 and STATUS is not Running, manually run get pods again
kubectl get pods -o wide > $PODS
if [ $? -ne 0 ]; then
	echo "ERROR: get pods info failed."
	echo "run 'kubectl get pods -o wide' manually in the terminal"
	exit 1
fi
echo "--------"
cat $NODES
echo "--------"
cat $PODS
echo "-----do you see READY 1/1, STATUS Running for interference $1 you are creating?"
echo "--------if NO, kill the jobs, then run 'kubectl get pods -o wide' manually in the terminal."

# workload
NAME2=("dedup" "blackscholes" "ferret" "freqmine" "canneal" "fft")
WORKLOAD="parsec-${NAME2[$(($2))]}"
echo "Running workload part2a/$WORKLOAD"
kubectl create -f parsec-benchmarks/part2a/$WORKLOAD.yaml
if [ $? -ne 0 ]; then
	echo "ERROR: parsec-benchmarks/part2a/$WORKLOAD.yaml create failed."
	exit 1
fi

echo "> interference num: $1	> workload num: $2"
echo "Manualy kill the process with ctrl-C when the job is completed."
echo "Then get the log using: ./getlog2a.sh $1 $2"
while true;
	do kubectl get jobs;
	sleep 20;
done

echo "!!!!! MUST delete the cluster after use: run ./delete.sh !!!!!"

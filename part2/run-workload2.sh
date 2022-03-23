# !/bin/bash

CURR=$PWD
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env2.sh
cd $PART2_YAML_PATH
echo ">>>>> You are in $PART2_YAML_PATH >>>>>"

if [ $# != 1 ] || [[ ! $1 =~ ^[0-9]+$ ]] || (($1 > 5))
then
	echo "Usage: ./run-workload2.sh <workload number>"
	echo "Workload number:"
	echo "- 0: dedup"
	echo "- 1: blackscholes"
	echo "- 2: ferret"
	echo "- 3: freqmine"
	echo "- 4: canneal"
	echo "- 5: fft"
	exit 1
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
echo "-----you should see READY 1/1, STATUS Running for al pods"
echo "--------if NO, kill the jobs with ./kill2.sh and run ./run2.sh again."

# workload
NAME2=("dedup" "blackscholes" "ferret" "freqmine" "canneal" "fft")
WORKLOAD="parsec-${NAME2[$(($2))]}"
echo "Running workload $WORKLOAD"
kubectl create -f parsec-benchmarks/part2a/$WORKLOAD.yaml

echo "Manualy kill the process with ctrl-C when the job is completed."
echo "Then get the log using: "
echo "  kubectl logs \$(kubectl get pods --selector=job-name=<JOB_NAME_PLACEHOLDER> --output=jsonpath='{.items[*].metadata.name}')"
while true;
	do kubectl get jobs;
	sleep 30;
done
echo "You can run ./kill2.sh to delete all jobs and pods."

echo "!!!!! MUST delete the cluster after use: run ./delete2.sh !!!!!"

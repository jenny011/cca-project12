# !/bin/bash

CURR=$PWD
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env2.sh
cd $PART2_YAML_PATH
echo ">>>>> You are in $PART2_YAML_PATH >>>>>"

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

if [[ $1 != "1" && $2 == "5" ]]
then
	echo "invalid pair of numbers"
	exit 1
fi

# workload
NAME2=("dedup" "blackscholes" "ferret" "freqmine" "canneal" "fft")
WORKLOAD="parsec-${NAME2[$(($2))]}"
echo "Running workload part2b/$1/$WORKLOAD"
kubectl create -f parsec-benchmarks/part2b/$1/$WORKLOAD.yaml
if [ $? -ne 0 ]; then
	echo "ERROR: parsec-benchmarks/part2b/$1/$WORKLOAD.yaml create failed."
	exit 1
fi

echo "> thd num: $1	> workload num: $2"
echo "Manualy kill the process with ctrl-C when the job is completed."
echo "Then get the log using: ./getlog2b.sh $1 $2"
while true;
	do kubectl get jobs;
	sleep 20;
done

echo "!!!!! MUST delete the cluster after use: run ./delete.sh !!!!!"

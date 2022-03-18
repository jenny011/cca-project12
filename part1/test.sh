# !/bin/bash

if [ $# -ne 1 ] || [[ ! $1 =~ ^[0-9]+$ ]] || (($1 > 6));
then
	echo "Usage: ./run.sh <a number>"
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

NAME=("cpu" "l1d" "l1i" "l2" "llc" "membw")
BENCHMARK="ibench-${NAME[$(($1 - 1))]}"
echo interference/$BENCHMARK.yaml

echo "!!!!! MUST delete the cluster after use: run delete_cluster.sh !!!!!"
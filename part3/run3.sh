# !/bin/bash

CURR=$PWD
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env3.sh
cd $PART3_YAML_PATH
echo ">>>>> You are in $PART3_YAML_PATH >>>>>"
# 0: dedup
# 1: blackscholes
# 2: ferret
# 3: freqmine
# 4: canneal
# 5: fft
NAME=("dedup" "blackscholes" "ferret" "freqmine" "canneal" "fft")

echo "Running parsec jobs"

for i in 4 2; do
	kubectl create -f part3-parsec/parsec-${NAME[$(($i))]}.yaml
	if [ $? -ne 0 ]; then
		echo "ERROR: ${NAME[$(($i))]} create failed."
		exit 1
	fi
done

kubectl get pods -o wide
sleep 30
kubectl get pods -o wide

for i in 0 1 5 3; do
	kubectl create -f part3-parsec/parsec-${NAME[$(($i))]}.yaml
	if [ $? -ne 0 ]; then
		echo "ERROR: ${NAME[$(($i))]} create failed."
		exit 1
	fi
done

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
echo "You can run ./kill3.sh to delete all jobs."

#kubectl get jobs;
while true;
	do kubectl get pods -o wide;
	sleep 20;
done

echo "!!!!! MUST delete the cluster after use: run ./delete.sh !!!!!"

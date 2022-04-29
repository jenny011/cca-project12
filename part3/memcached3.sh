# !/bin/bash

CURR=$PWD
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env3.sh
cd $PART3_YAML_PATH
echo ">>>>> You are in $PART3_YAML_PATH >>>>>"

echo "Running memcached"
# Run memcached
kubectl create -f part3-memcached.yaml
if [ $? -ne 0 ]; then
	echo "ERROR: create part3-memcached.yaml failed."
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
echo "You can run ./kill3.sh to delete all jobs."

echo "!!!!! MUST delete the cluster after use: run ./delete.sh !!!!!"

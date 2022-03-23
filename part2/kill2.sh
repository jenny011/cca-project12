# !/bin/bash

CURR=$PWD
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env2.sh
cd $PART2_YAML_PATH
echo ">>>>> You are in $PART2_YAML_PATH >>>>>"

echo "Deleting all jobs and pods..."
kubectl delete jobs --all 
kubectl delete pods --all

echo "!!!!! MUST delete the cluster after use: run ./delete2.sh !!!!!"
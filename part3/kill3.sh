# !/bin/bash

CURR=$PWD
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env3.sh
cd $PART3_YAML_PATH
echo ">>>>> You are in $PART3_YAML_PATH >>>>>"

echo "Deleting all jobs and pods..."
kubectl get pods -o json > ../part3/parsec-time/parsec.json
kubectl delete jobs --all
kubectl get pods
# kubectl delete pods --all

echo "!!!!! MUST delete the cluster after use: run ./delete.sh !!!!!"

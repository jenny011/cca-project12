# !/bin/bash

if [ "$#" != 1 ] || [[ "$1" != "a" && "$1" != "b" ]]
then
	echo "Usage: ./deploy2.sh <part number>"
	echo "Part number:"
	echo "- a: part2a"
	echo "- b: part2b"
	exit 1
fi

CURR=$PWD
source $CURR/env2.sh

cd $PART2_YAML_PATH
echo ">>>>> You are in $PART2_YAML_PATH >>>>>"

# Create a kubernetes cluster with 1 master and 2 nodes
PROJECT=`gcloud config get-value project`
kops create -f part2$1.yaml
if [ $? -ne 0 ]; then
	echo "ERROR: part2$1.yaml create failed. Have you replaced the placeholders in part2$1.yaml?"
	exit 1
fi

# Deploy a cluster using "kops"
echo ">>>>> Deploying cluster... >>>>>"
echo "!!!!! MUST delete the cluster after use: run ./delete.sh !!!!!"
kops update cluster part2$1.k8s.local --yes --admin

# Wait until the cluster is ready to use
echo ">>>>> Wait until the cluster is ready... >>>>>"
echo ">>>>> You'll see many failures and errors until it's ready >>>>>"
kops validate cluster --wait 10m
if [ $? -ne 0 ]; then
	echo "ERROR: cluster validate failed."
	exit 1
fi

echo ">>>>> Cluster Ready! >>>>>"
echo "!!!!! MUST delete the cluster after use: run ./delete.sh !!!!!"

# Output nodes info to a file
kubectl get nodes -o wide > $NODES
if [ $? -ne 0 ]; then
	echo "run 'kubectl get nodes -o wide > <your-path-to-pods-output-file>' manually in the terminal"
	echo "ERROR: get nodes info failed."
	exit 1
fi
echo "--------"
cat $NODES
echo "--------"
echo ">>>>> Now you can ssh into parsec-server in new terminal windows"
echo "gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@parsec-server-<PLACEHOLDER> --zone europe-west3-a"

echo ">>>>> Run experiments with ./run-interference2.sh"

echo "!!!!! MUST delete the cluster after use: run ./delete.sh !!!!!"


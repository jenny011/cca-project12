# !/bin/bash

CURR=$PWD
source $CURR/env4.sh

cd $PART4_YAML_PATH
echo ">>>>> You are in $PART4_YAML_PATH >>>>>"

# Create a kubernetes cluster with 1 master and 2 nodes
PROJECT=`gcloud config get-value project`
kops create -f part4.yaml
if [ $? -ne 0 ]; then
	echo "ERROR: part4.yaml create failed. Have you replaced the placeholders in part4.yaml?"
	exit 1
fi

# Create secret
kops create secret --name part4.k8s.local sshpublickey admin -i ~/.ssh/cloud-computing.pub
if [ $? -ne 0 ]; then
	echo "ERROR: secret create failed."
	exit 1
fi

# Deploy a cluster using "kops"
echo ">>>>> Deploying cluster... >>>>>"
echo "!!!!! MUST delete the cluster after use: run ./delete.sh !!!!!"
kops update cluster --name part4.k8s.local --yes --admin

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
echo "Manually install memcached on memcache-server"
echo "gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@<NAME> --zone europe-west3-a"

echo "!!!!! MUST delete the cluster after use: run ./delete.sh !!!!!"

# !/bin/bash

CURR=$PWD
source $CURR/env1.sh

cd $PART1_YAML_PATH
echo ">>>>> You are in $PART1_YAML_PATH >>>>>"

# Create a kubernetes cluster with 1 master and 2 nodes
PROJECT=`gcloud config get-value project`
kops create -f part1.yaml
if [ $? -ne 0 ]; then
	echo "ERROR: part1.yaml create failed."
	exit 1
fi

# Create secret
kops create secret --name part1.k8s.local sshpublickey admin -i ~/.ssh/cloud-computing.pub
if [ $? -ne 0 ]; then
	echo "ERROR: secret create failed."
	exit 1
fi

# Deploy a cluster using "kops"
echo ">>>>> Deploying cluster... >>>>>"
echo "!!!!! MUST delete the cluster after use: run delete_cluster.sh !!!!!"
kops update cluster --name part1.k8s.local --yes --admin

# Wait until the cluster is ready to use
echo ">>>>> Wait until the cluster is ready... >>>>>"
echo ">>>>> You'll see many failures and errors until it's ready >>>>>"
kops validate cluster --wait 10m
if [ $? -ne 0 ]; then
	echo "ERROR: cluster validate failed."
	exit 1
fi

echo ">>>>> Cluster Ready! >>>>>"

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
echo "Now you can ssh into client-agent and client-measure in new terminal windows"
echo "gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-agent-<placeholder> --zone europe-west3-a"
echo "gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-measure-<placeholder> --zone europe-west3-a"

# Run memcached
kubectl create -f memcache-t1-cpuset.yaml
if [ $? -ne 0 ]; then
	echo "ERROR: create memcache-t1-cpuset.yaml failed."
	exit 1
fi

kubectl expose pod some-memcached --name some-memcached-11211 --type LoadBalancer --port 11211 --protocol TCP
if [ $? -ne 0 ]; then
	echo "ERROR: expose pod failed."
	exit 1
fi

sleep 60
kubectl get service some-memcached-11211
if [ $? -ne 0 ]; then
	echo "ERROR: get service failed."
	exit 1
fi

echo "!!!!! MUST delete the cluster after use: run delete_cluster.sh !!!!!"


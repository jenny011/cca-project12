# !/bin/bash
### LOCAL machine
### For macOS

# Do these manually ONCE
# 1. add to .bashrc: export PATH=$PATH:<your-path>/google-cloud-sdk/bin
# 2. `gcloud init` with cca-eth-2022-group-4, do NOT configure any default computer region and zone
# 3. `gcloud compute zones list` to enable compute engine API
# 4. `gcloud auth application-default login` to configure your default credentials
# 5. cd ~/.ssh
# 6. ssh-keygen -t rsa -b 4096 -f cloud-computing


# Fill in env1.sh with your values BEFORE you run this script


CURR=$PWD
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env1.sh

echo "Run it only ONCE"
# Create an empty bucket to store the configuration for your clusters
gsutil mb $KOPS_STATE_STORE
if [ $? -ne 0 ]; then
	echo "ERROR: KOPS_STATE_STORE create failed."
	exit 1
fi

# This is done already in env1.sh
# export KOPS_STATE_STORE=gs://cca-eth-2022-group-XXX-ethzid/

# Connect to agent and measure nodes
# ssh into agent
# gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-agent-<placeholder> --zone europe-west3-a
# ssh into measure
# gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@client-measure-<placeholder> --zone europe-west3-a

# Run experiments
# Run "run1.sh"

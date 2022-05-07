# !/bin/bash

CURR=$PWD
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env4.sh

cd $PART4_YAML_PATH
echo ">>>>> You are in $PART4_YAML_PATH >>>>>"

kops delete cluster part4.k8s.local --yes
if [ $? -ne 0 ]; then
	echo "ERROR: DANGEROUS!!! delete cluster failed."
	exit 1
fi

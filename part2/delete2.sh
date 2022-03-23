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
# Export all the environmental vars (including your ethzid)
# comment it out if exported
source $CURR/env2.sh

cd $PART2_YAML_PATH
echo ">>>>> You are in $PART2_YAML_PATH >>>>>"


echo "You are deleting >>>part2$1<<< cluster!"
kops delete cluster part2$1.k8s.local --yes
if [ $? -ne 0 ]; then
	echo "ERROR: DANGEROUS!!! delete cluster part2$1 failed."
	exit 1
fi
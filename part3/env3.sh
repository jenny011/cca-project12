# !/bin/bash

BASEDIR=/Users/jenny/Desktop/project12/part3

export KOPS_STATE_STORE=gs://cca-eth-2022-group-4-jinzhu/
export KOPS_FEATURE_FLAGS=AlphaAllowGCE
export PART3_YAML_PATH="/Users/jenny/Desktop/project12/config"
export NODES="$BASEDIR/nodes.txt"
export PODS="$BASEDIR/pods.txt"

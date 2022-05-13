# !/bin/bash

CURRDIR=$(PWD)
BASEDIR=$(dirname $CURRDIR)

export KOPS_STATE_STORE=gs://cca-eth-2022-group-004-jinzhu/
export KOPS_FEATURE_FLAGS=AlphaAllowGCE
export PART3_YAML_PATH="$BASEDIR/config"
export NODES="$BASEDIR/nodes.txt"
export PODS="$BASEDIR/pods.txt"

# !/bin/bash

BASEDIR=$PWD
PARENTDIR=$(dirname $BASEDIR)

export KOPS_STATE_STORE=gs://cca-eth-2022-group-004-jiahzhang/
export KOPS_FEATURE_FLAGS=AlphaAllowGCE
export PART4_YAML_PATH="$PARENTDIR/config"
export NODES="$BASEDIR/nodes.txt"
export PODS="$BASEDIR/pods.txt"

# !/bin/bash

BASEDIR=<your-path-to-nodes-and-pods>

export KOPS_STATE_STORE=gs://cca-eth-2022-group-4-<ethzid>/
export KOPS_FEATURE_FLAGS=AlphaAllowGCE
export PART1_YAML_PATH="<your-path-to>/cloud-comp-arch-project"
export NODES="$BASEDIR/nodes.txt"
export PODS="$BASEDIR/pods.txt"
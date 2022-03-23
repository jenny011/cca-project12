# !/bin/bash

BASEDIR=<path-to-nodes-and-pods-dot-txt>

export KOPS_STATE_STORE=gs://cca-eth-2022-group-4-<ETHZID>/
export KOPS_FEATURE_FLAGS=AlphaAllowGCE
export PART2_YAML_PATH="<PATH_TO>/cloud-comp-arch-project"
export NODES="$BASEDIR/nodes.txt"
export PODS="$BASEDIR/pods.txt"
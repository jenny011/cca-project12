# PART 2

## Do these ONCE
1. If you haven't done "PART 1-Do these ONCE" yet, do them once.
2. Fill in env2.sh

## Preparation
1. If you deleted or haven't created your bucket, run `./setup2.sh` to create it.

## Run experiments
1. `./deploy2.sh <a OR b>`: deploy the cluster for "part2a" or "part2b", the cluster should be running if no errors.
2. ssh into parsec-server
3. `./run-interference2.sh <interference number>`: run interference
4. `./run-workload2.sh <workload number>`: run workload
5. `./kill2.sh <benchmark number>`: teardown benchmark
6. `./delete2.sh <a OR b>`: delete the cluster, MUST do if finished using cluster
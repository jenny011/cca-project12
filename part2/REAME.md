# PART 2

## Do these ONCE
1. If you haven't done "PART 1-Do these ONCE" yet, do them once.
2. Fill in env2.sh

## Preparation
1. If you deleted or haven't created your bucket, run `./setup2.sh` to create it.

## Run experiments
1. `./deploy2.sh <a OR b>`: deploy the cluster for "part2a" or "part2b", the cluster should be running if no errors.
2. ssh into parsec-server
3. `./run2a.sh <interference number> <workload number>`: run 2a experiment with interference
4. `./getlog2a.sh <interference number> <workload number>`: output 2a log to data file
5. `./run2b.sh <thread number> <workload number>`: run 2b scaling experiment with no interference
6. `./getlog2b.sh <thread number> <workload number>`: output 2b log to data file
7. `./kill2.sh`: teardown all jobs and pods
8. `./delete.sh <a OR b>`: delete the cluster, MUST do if finished using cluster
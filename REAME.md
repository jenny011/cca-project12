# CCA Project Part 1 and 2

## PART 1

1. `chmod +x <every>.sh`
2. Fill in env.sh
3. `./setup1.sh` only once
4. `./deploy1.sh`: deploy the cluster, the cluster should be running if no errors.
5. ssh into client-agent and client-measure
6. `./run1.sh <benchmark number>`: setup benchmark
7. `./kill.sh <benchmark number>`: teardown benchmark
8. `./delete_cluster.sh`: delete the cluster, MUST do if finished using cluster
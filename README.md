# CCA Project Part 1 and 2

## Notice
"interference-parsec" folder does NOT exist in cloud-comp-arch-project.\
I created it for part2a and part2b. Copy the folder into your cloud-comp-arch-project.

## PART 1

### Do these ONCE
1. add to .bashrc: export PATH=$PATH:<your-path>/google-cloud-sdk/bin
2. `gcloud init` with cca-eth-2022-group-4, do NOT configure any default computer region and zone
3. `gcloud compute zones list` to enable compute engine API
4. `gcloud auth application-default login` to configure your default credentials
5. cd ~/.ssh
6. ssh-keygen -t rsa -b 4096 -f cloud-computing
7. `chmod +x <every>.sh`
8. Fill in env1.sh

### Preparation

2. If you deleted or haven't created your bucket, run `./setup1.sh` to create it.

### Run experiments
1. `./deploy1.sh`: deploy the cluster, the cluster should be running if no errors.
2. ssh into client-agent and client-measure
3. `./run1.sh <benchmark number>`: run benchmark
4. `./kill1.sh <benchmark number>`: teardown benchmark
5. `./delete1.sh`: delete the cluster, MUST do if finished using cluster

## PART 2

### Do these ONCE
1. If you haven't done "PART 1-Do these ONCE" yet, do them once.
2. Fill in env2.sh

### Preparation
1. If you deleted or haven't created your bucket, run `./setup2.sh` to create it.

### Run experiments
1. `./deploy2.sh <a OR b>`: deploy the cluster for "part2a" or "part2b", the cluster should be running if no errors.
2. ssh into parsec-server
3. `./run-interference2.sh <interference number>`: run interference
4. `./run-workload2.sh <workload number>`: run workload
5. `./kill2.sh`: teardown benchmark
6. `./delete2.sh <a OR b>`: delete the cluster, MUST do if finished using cluster
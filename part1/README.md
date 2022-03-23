# CCA Project Part 1 and 2

## PART 1

## Do these ONCE
1. add to .bashrc: export PATH=$PATH:<your-path>/google-cloud-sdk/bin
2. `gcloud init` with cca-eth-2022-group-4, do NOT configure any default computer region and zone
3. `gcloud compute zones list` to enable compute engine API
4. `gcloud auth application-default login` to configure your default credentials
5. cd ~/.ssh
6. ssh-keygen -t rsa -b 4096 -f cloud-computing
7. `chmod +x <every>.sh`
8. Fill in env1.sh

### Preparation
1. If you deleted or haven't created your bucket, run `./setup1.sh` to create it.

## Run experiments
1. `./deploy1.sh`: deploy the cluster, the cluster should be running if no errors.
2. ssh into client-agent and client-measure
3. `./run1.sh <benchmark number>`: run benchmark
4. `./kill1.sh <benchmark number>`: teardown benchmark
5. `./delete1.sh`: delete the cluster, MUST do if finished using cluster

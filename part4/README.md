# CCA Project Part 4

## PART 4

## Do these ONCE
1. add to .bashrc: export PATH=$PATH:<your-path>/google-cloud-sdk/bin
2. `gcloud init` with cca-eth-2022-group-4, do NOT configure any default computer region and zone
3. `gcloud compute zones list` to enable compute engine API
4. `gcloud auth application-default login` to configure your default credentials
5. cd ~/.ssh
6. ssh-keygen -t rsa -b 4096 -f cloud-computing
7. `chmod +x <every>.sh`
8. Fill in env4.sh

### Preparation
1. If you deleted or haven't created your bucket, run `./setup4.sh` to create it.

## Run experiments
1. `./deploy4.sh`: deploy the cluster, the cluster should be running if no errors.
2. ssh into client-agent and client-measure\
See agent.txt\
You can fill in `export ...IP=` in measure.txt and export them in client-measure\
3. setup memcached server:\
See memcached-server.txt\
start/status/stop a system service (memcached, docker): `sudo systemctl start/status/stop <service>`\
Use python3 for everything\
    + install pip3\
    + install python packages: docker, psutil\
Give docker permission to $USER
4. `./delete.sh`: delete the cluster, MUST do if finished using cluster

## TODO
Add controller code for scheduling and dynamic updating.

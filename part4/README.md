# CCA Project Part 4

## NOTICE
PLEASE read through this document because it explains the infrastructure for part4 step by step.\
PLEASE describe your scheduling policies, changes to the code, analysis and questions in this document or in some other shared files/directory.\
Thank you!\

WATCH OUT FOR BUGS!\
1. I have NOT checked whether the controller correctly detects that all the containers are empty and correctly exits!\
Ideally: `scheduler.group_done` and `scheduler.all_done` should work correctly and the controller should exit with at least as many cores assigned to memcached as you need.\
IMPORTANT: In your first complete run, please periodically (every 5-10 minutes) check container status with `docker ps --all` to see whether the jobs finished (containers exited).
2. I have NOT checked whether the latest version of `scheduler.update_group()` works, although I think it should work.
3. I have NOT checked whether anything related to `pause/unpause_container/group()` works because I did not experiment with related scheduling policies.
4. I have NOT checked whether the container exit event is correctly timed and saved in `is_exited()`, although I think it should work.


## PART 4
For part4-2, 4-3 and 4-4, use `deploy4.sh` to start the cluster and then work directly in the vms.

### TODO
Our total runtime is longer than running everything together on all cores.\
Our memcached SLO violation is high.
1. IMPORTANT: Find a policy that does not leave CPUs idle after jobs finish.
2. Find good cpu_util thresholds and a good time interval.
2. Optimize the data structure, its initialization and clean-up of `scheduler.queue` if you want to use it.
3. Anything you'd like to add/change.

### How to setup the nodes
+ memcache-server: memcache-server.txt\
"line x-y" refers to memcache-server.txt\
ssh into the vm\
`$ vim setup.sh`\
copy-paste line 5-13 into setup.sh\
`$ chmod +x setup.sh`\
`$ ./setup.sh`\
config memcached: line 15-18\
restart memcached: line 20\
check that #threads = 6 + t\
copy controller folder to memcache-server: line 28, use the your path and node id\
copy data back to local: line 33, use your path and node id

+ agent and measure: client.txt\
"line x-y" refers to client.txt\
ssh into the vms\
`$ vim setup.sh`\
copy-paste line 5-11 into setup.sh\
`$ chmod +x setup.sh`\
`$ ./setup.sh`\
execute line 10\
execute line 14-15 with the correct IPs in client-measure node\
run the corresponding lines in corresponding vms

### How to use the Controller
Always use python3\
`python3 prepare.py` to pull the images\
`taskset -c 2,3 python3 run.py` to run the controller on cpus that memcached does not use. If memcached runs on all cpus, then ignore "taskset".\
You should ONLY start client-measure and client-agent AFTER you see that memcached cpu affinity is set to 0 (the first block of outputs) because it starts with all 4 cores. Might want to change this setup?\
To get correct measurements, if you stop the controller with ctrl-C, you should stop and remove the containers manually before you start your next measurement. Might not be necessary for debugging/performance debugging purpose, but it dependes.

### Output measurements
Measurements are automatically collected by the controller at runtime.\
You need to copy the data from memcached server to your local machine, as mentioned above.\
All experiment data is in $HOME/data by default, which is why you need to `mkdir data` in ~/ of the memcached server.\
Every time you run controller/run.py, a data folder is created under $HOME/data. The data folder is labeled by the time you run the controller (month_date_hour_minute_second).\
IMPORTANT: You need to keep track of which data folder is contains useful data because you can easily run the controller too many times and generate too many data folers. Or you can improve the automatic labelling in run.py.\
Each data folder contains a file for memcached, a file for parsec jobs and a file containing start/end time of the controller.


### Controller
All code in ./controller
+ Timer.py:
    - Timer class with separate timers for memcached and parsec jobs.
    - writes to timed events to separate files.

+ Container.py: for parsec jobs
    - Container class with wrappers for operations on single container
    - uses the timer to time container operations

+ Scheduler.py: for groups of parsec jobs
    - Scheduler class that wraps container operations on a group of list_containers
    - it also has a queue of batches of events. The first non-empty batch is allowed to use the additional cpu. `TODO`: Optimize the data structure, its initialization and clean-up.

+ Memcached.py: for memcached
    - Memcached class that wraps operations on memcached
    - uses the timer to time memcached operations

+ Controller.py: the controller
    - contains a Memcached instance and a Scheduler instance
    - the periodic_scheduler() method obtains the cpu_utilizations and requests config updates if needed and checks if all jobs are finished every x second.
    - memcached process cpu util is almost always slightly less than the total cpu util of the cpus which memcached runs on, which is reasonable

+ run.py:
    - init controller and run it.

Two config files\
+ containers.json: initial config of containers
+ groups.json: lists of groups of parsec jobs


### Docker command line
If you need them\
docker ps --all\
docker container ls --all\
docker stop [container names]\
docker rm [container names]


### Do these ONCE
1. add to .bashrc: export PATH=$PATH:[your-path]/google-cloud-sdk/bin
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
See client.txt\
You can fill in `export ...IP=` in client.txt and export them in client-measure\
3. ssh into memcached server if you need to:\
See memcached-server.txt\
start/status/stop a system service (memcached, docker): `sudo systemctl start/status/stop <service>`\
Use python3 for everything\
    + install pip3\
    + install python packages: docker, psutil\
Give docker permission to $USER
4. `./delete.sh`: delete the cluster, MUST do if finished using cluster

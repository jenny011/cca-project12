# CCA Project Part 3

## PART 3

## Do these ONCE
1. add to .bashrc: export PATH=$PATH:<your-path>/google-cloud-sdk/bin
2. `gcloud init` with cca-eth-2022-group-4, do NOT configure any default computer region and zone
3. `gcloud compute zones list` to enable compute engine API
4. `gcloud auth application-default login` to configure your default credentials
5. cd ~/.ssh
6. ssh-keygen -t rsa -b 4096 -f cloud-computing
7. `chmod +x <every>.sh`
8. Fill in env3.sh

### Preparation
1. If you deleted or haven't created your bucket, run `./setup3.sh` to create it.

## Run experiments
1. `./deploy3.sh`: deploy the cluster, the cluster should be running if no errors.
2. ssh into client-agent-a, agent-b and client-measure\
You can fill in `export ...IP=` in measure.txt and export them in client-measure\
Modify config/part3-parsec files to reflect your scheduling\
Modify run3.sh to start the jobs according to your scheduling\
Remember to `sleep`, o.w. the jobs are not started in the correct order.
3. `./run3.sh`: run parsecs\
Now, save memcached measurements on "measure" node.
4. `./kill3.sh`: save parsec runtime and teardown parsec and memcached\
!!!Remember to rename parsec-time/parsec.json with the proper number, o.w. it will be overwritten!!!\
To start memcached again, run `./memcached3.sh`
5. `./delete.sh`: delete the cluster, MUST do if finished using cluster

## Notice
"scheduling.txt" contains measurements from part1 and 2 for quick reference.\
Make sure to request less than all cpus (eg. 7.5 for 8 core machine) to give enough cpu time for background processes.\
If a job stays pending, then the its configuration most likely doesn't fit on the machine.\
Test your config only ONCE to save money.\
Add your best results (close ones all count) to "part3-results".\
We can then run the best configs 3 times.


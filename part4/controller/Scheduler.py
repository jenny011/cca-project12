import os, sys, json
from Container import *

class Scheduler():
    def __init__(self, timer, jobs_config, groups_config):
        with open(jobs_config, "r") as jobs:
            self.jobs = json.load(jobs)
        with open(groups_config, "r") as groups:
            self.groups = json.load(groups)
            
        self.ci = ContainerInterface()
        self.timer = timer

        for job in self.jobs.values():
            self.ci.create_container(job)

    # def config_jobs(self, config_file):
    #     with open(config_file, "r") as config:
    #         self.jobs = json.load(config)
    #
    # def config_groups(self, config_file):
    #     with open(config_file, "r") as config:
    #         self.groups = json.load(config)
    #     # for k in self.groups.keys():
    #     #     self.groups[int[k]] = self.groups.pop(k)

    # def init_jobs(self):
    #     for job in self.jobs.values():
    #         self.ci.create_container(job)
    #     self.ci.list_containers(self.jobs.keys())

    def start_group(self,group_id, cpus):
        for job in self.groups[group_id]:
            self.ci.start_container(job, cpus)

    def pause_group(self,group_id):
        for job in self.groups[group_id]:
            self.ci.pause_container(job)

    def unpause_group(self,group_id):
        for job in self.groups[group_id]:
            self.ci.unpause_container(job)

    def stop_group(self,group_id):
        for job in self.groups[group_id]:
            self.ci.stop_container(job)

    def update_group(self,group_id, cpus):
        for job in self.groups[group_id]:
            self.ci.update_container(job, cpus)

    def print_jobs(self):
        print("-------jobs-------")
        for k,v in self.jobs.items():
            print(f"{k}: {v['command']}\tcpu{v['cpuset_cpus']}")

    def print_groups(self):
        print("-------groups-------")
        for k,v in self.groups.items():
            print(f"queue{k}: {v}")

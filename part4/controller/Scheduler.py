import os, sys, json
from Container import *

class Scheduler():
    def __init__(self):
        self.containers = {}
        self.groups = {}
        self.ci = ContainerInterface()

    def config_containers(self, config_file):
        with open(config_file, "r") as config:
            self.containers = json.load(config)

    def config_groups(self, config_file):
        with open(config_file, "r") as config:
            self.groups = json.load(config)
        for k in self.groups.keys():
            self.groups[int(k)] = self.groups.pop(k)

    def init_containers(self):
        self.ci.create_containers(self.containers.values())
        self.ci.list_containers(self.containers.keys())

    def schedule_containers(self, queue_id):
        for job in self.groups[queue_id]:
            print(job)

    def print_containers(self):
        print("-------containers-------")
        for k,v in self.containers.items():
            print(f"{k}: {v['command']}\tcpu{v['cpuset_cpus']}")

    def print_groups(self):
        print("-------groups-------")
        for k,v in self.groups.items():
            print(f"queue{k}: {v}")

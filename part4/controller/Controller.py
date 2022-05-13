import os, sys, json
import psutil, subprocess
from Scheduler import *
from Memcached import *
from Timer import *

class Controller():
    def __init__(self, expnum, jobs_config, groups_config):
        self.cpu_count = psutil.cpu_count(logical=True)
        self.timer = Timer(expnum)
        self.memcached = Memcached(self.timer)
        self.scheduler = Scheduler(self.timer, jobs_config, groups_config)

    # def init_memcached(self):
    #     self.memcached.get_process()
    #
    # def init_scheduler(self):
    #     self.scheduler.config_jobs(jobs_config)
    #     self.scheduler.init_jobs()
    #     self.scheduler.config_groups(groups_config)

    def print_scheduler(self):
        self.scheduler.print_jobs()
        self.scheduler.print_groups()

    def print_memcached(self):
        print(self.memcached)

    def start_jobs(self):
        for i in range(2):
            print("Starting group", str(i), "on cpu", str(i+2))
            self.scheduler.start_group(str(i), str(i+2))

    def periodic_scheduler(self):
        # https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
        per_core_cpu_usage = psutil.cpu_percent(interval=None, percpu=True)
        mc_cpu_usage = self.memcached.get_cpu_percent()
        print("per core:", per_core_cpu_usage)
        print("memcached:", mc_cpu_usage)

        core_01_cpu_usage = per_core_cpu_usage[0] + per_core_cpu_usage[1]
        print("cpu 01 util:" core_01_cpu_usage)

        # set memcached cpu affinity
        if core_01_cpu_usage <= 75:
            memcached.set_cpu(1)
            # update container
            print("Update group", "0", "to cpu", "1,2")
            self.scheduler.update_group("0", "1,2")
        else:
            # update container
            print("Update group", "0", "to cpu", "2")
            self.scheduler.update_group("0", "2")
            memcached.set_cpu(2)

import os, sys, json
import psutil, subprocess
from Scheduler import *
from Memcached import *

class Controller():
    def __init__(self):
        self.cpu_count = psutil.cpu_count(logical=True)
        self.memcached = Memcached()
        self.scheduler = Scheduler()

    def init_memcached(self):
        self.memcached.get_process()

    def init_scheduler(self, container_config, queue_config):
        self.scheduler.config_containers(container_config)
        self.scheduler.init_containers()
        self.scheduler.config_groups(queue_config)

    def print_scheduler(self):
        self.scheduler.print_containers()
        self.scheduler.print_groups()

    def print_memcached(self):
        print(self.memcached)

    def periodic_scheduler(self):
        # https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
        per_core_cpu_usage = psutil.cpu_percent(interval=None, percpu=True)
        mc_cpu_usage = self.memcached.get_cpu_percent()
        print("per core:", per_core_cpu_usage)
        print("memcached:", mc_cpu_usage)

        # for i in range(self.cpu_count):
        #     if per_core_cpu_usage[i] < 0.2:
        #         self.memcached.adjust_cpu(1)
        #         self.scheduler.start_containers(0)
        #     elif per_core_cpu_usage[i] < 0.5:
        #         pass
        #     else:
        #         self.memcached.adjust_cpu(2)
        #         self.scheduler.stop_containers(0)

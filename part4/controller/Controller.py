import os, sys, json
from Scheduler import *
from Memcached import *

class Controller():
    def __init__(self):
        self.memcached = Memcached()
        self.scheduler = Scheduler()

    def init_memcached(self):
        self.memcached.get_pid()

    def init_scheduler(self, container_config, queue_config):
        self.scheduler.config_containers(container_config)
        self.scheduler.init_containers()
        self.scheduler.config_groups(queue_config)

    def print_scheduler(self):
        self.scheduler.print_containers()
        self.scheduler.print_groups()

    def print_memcached(self):
        print(self.memcached)

import os, sys, json
import psutil, subprocess
# https://psutil.readthedocs.io/en/latest/#
from Timer import *

class Memcached():
    def __init__(self, timer):
        self.name = "memcached"
        self.cpu = 0
        self.timer = timer
        for proc in psutil.process_iter():
            if self.name in proc.name():
               self.p = proc
               break
        self.set_cpu()
        print("memcached initialized")

    def get_cpu_percent(self):
        return self.p.cpu_percent(interval=None)

    def set_cpu(self, cpu_num=2):
        # print("mc:", self.cpu, cpu_num)
        if self.cpu != cpu_num:
            self.cpu = cpu_num
            cpu_list = ",".join([str(i) for i in range(self.cpu)])
            subprocess.run(["sudo", "taskset", "-a", "-cp", cpu_list, str(self.p.pid)])
            print(">>> Update mc:", self.cpu, "to cpu list", cpu_list)
        self.timer.record_mc(cpu_num)

    def __repr__(self):
        return f"PID:{self.p.pid}, nCPU:{self.cpu}"

import os, sys, json
import psutil, subprocess
# https://psutil.readthedocs.io/en/latest/#

class Memcached():
    def __init__(self):
        self.name = "memcached"
        self.p = None
        self.cpu = 1

    def get_process(self):
        for proc in psutil.process_iter():
            if self.name in proc.name():
               self.p = proc
               break
        # self.pid = int(subprocess.check_output(["pidof","-s",self.name]))
        self.set_cpu()

    def get_cpu_percent(self):
        return self.p.cpu_percent(interval=None)

    def set_cpu(self):
        cpu_list = ",".join([str(i) for i in range(self.cpu)])
        subprocess.run(["sudo", "taskset", "-a", "-cp", cpu_list, str(self.p.pid)])

    def adjust_cpu(self, cpu_num):
        self.cpu = cpu_num
        self.set_cpu()

    def __repr__(self):
        return f"PID:{self.p.pid}, nCPU:{self.cpu}"

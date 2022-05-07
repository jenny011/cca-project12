import os, sys, json
import psutil, subprocess

class Memcached():
    def __init__(self):
        self.name = "memcached"
        self.pid = None
        self.cpu = 1

    def get_pid(self):
        for proc in psutil.process_iter():
            if self.name in proc.name():
               self.pid = proc.pid
               break
        # self.pid = int(subprocess.check_output(["pidof","-s",self.name]))
        self.set_cpu()

    def set_cpu(self):
        cpu_list = ",".join([str(i) for i in range(self.cpu)])
        subprocess.run(["sudo", "taskset", "-a", "-cp", cpu_list, str(self.pid)])

    def adjust_cpu(self):
        self.cpu = 2
        self.set_cpu()

    def __repr__(self):
        return f"PID:{self.pid}, nCPU:{self.cpu}"

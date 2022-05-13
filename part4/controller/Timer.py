import time
import subprocess

class Timer():
    def __init__(self, expnum):
        self.mc_f=f"~/data/{expnum}/memcached.csv"
        self.jobs_f=f"~/data/{expnum}/jobs.csv"
        subprocess.run(["mkdir", f"~/data/{expnum}"])

    def record_mc(self, cpu_num):
        t = time.time()
        with open(self.mc_f) as f:
            f.write(f"t,{cpu_num}")

    def record_job(self, name, event):
        t = time.time()
        with open(self.jobs_f) as f:
            f.write(f"{name},t,{event}")

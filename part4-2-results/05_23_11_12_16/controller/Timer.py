import time
import subprocess

class Timer():
    def __init__(self, expnum):
        subprocess.run(["mkdir", f"/home/ubuntu/data/{expnum}"])
        self.mc_f = open(f"/home/ubuntu/data/{expnum}/memcached.csv", 'a')
        self.jobs_f = open(f"/home/ubuntu/data/{expnum}/jobs.csv", 'a')
        self.controller_f = f"/home/ubuntu/data/{expnum}/controller.csv"
        self.controller_start_t = time.time()

    def record_mc(self, cpu_num):
        t = time.time()
        self.mc_f.write(f"{t},{cpu_num}\n")

    def record_job(self, name, event, cpus=""):
        t = time.time()
        self.jobs_f.write(f"{name},{t},{event},{cpus}\n")

    def destroy_timer(self):
        with open(self.controller_f, 'a') as f:
            f.write(f"Controller start time,{self.controller_start_t}\n")
            f.write(f"Controller end time,{time.time()}\n")
        self.mc_f.close()
        self.jobs_f.close()

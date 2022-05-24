import time
import subprocess

class Timer():
    def __init__(self, expnum):
        subprocess.run(["mkdir", f"/home/ubuntu/data/{expnum}"])
        self.mc_f = f"/home/ubuntu/data/{expnum}/memcached.csv"
        self.jobs_f = f"/home/ubuntu/data/{expnum}/jobs.csv"
        self.controller_f = f"/home/ubuntu/data/{expnum}/controller.csv"
        self.controller_start_t = time.time()
        self.mc_data = ""
        self.jobs_data = ""

    def record_mc(self, cpu_num):
        t = time.time()
        self.mc_data += f"{t},{cpu_num}\n"

    def record_job(self, name, event, cpus=""):
        t = time.time()
        self.jobs_data += f"{name},{t},{event},{cpus}\n"


    def destroy_timer(self):
        with open(self.controller_f, 'a') as f:
            f.write(f"Controller start time,{self.controller_start_t}\n")
            f.write(f"Controller end time,{time.time()}\n")
        with open(self.mc_f, 'a') as f:
            f.write(self.mc_data)
        with open(self.jobs_f, 'a') as f:
            f.write(self.jobs_data)

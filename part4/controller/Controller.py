import os, sys, json, time
import psutil, subprocess
from Scheduler import *
from Memcached import *
from Timer import *

class Controller():
    def __init__(self, expnum, jobs_config, groups_config):
        self.cpu_count = psutil.cpu_count(logical=True)
        self.timer = Timer(expnum)
        self.memcached = Memcached(self.timer)
        print(self.memcached)
        self.scheduler = Scheduler(self.timer, jobs_config, groups_config)
        self.scheduler.print_containers()

    def start_jobs(self):
        for i in range(2):
            print("Starting group", str(i))
            self.scheduler.start_group(str(i))

    def new_periodic_scheduler(self):

        # run ferret, freqmine, blackscholes, dedup
        cur_job = 0
        self.scheduler.start_one(cur_job)
        while True:
            per_core_cpu_util = psutil.cpu_percent(interval=None, percpu=True)
            mc_prc_cpu_util = self.memcached.get_cpu_percent()
            print("per core:", per_core_cpu_util)
            print("memcached:", mc_prc_cpu_util)

            mc_cpu_util = per_core_cpu_util[0]
            if self.memcached.cpu == 2:
                mc_cpu_util += per_core_cpu_util[1]
            print("mc cpu util:", mc_cpu_util)

            if mc_prc_cpu_util <= 70:
                self.memcached.set_cpu(1)
                self.scheduler.update_one(cur_job, False)
            else:
                self.scheduler.update_one(cur_job, True)
                self.memcached.set_cpu(2)
            if self.scheduler.is_finished(cur_job):
                cur_job += 1
                if cur_job <= 3:
                    self.scheduler.start_one(cur_job)
                else:
                    break
            time.sleep(0.5)

        # run canneal and fft
        self.scheduler.start_one(4)
        self.scheduler.start_one(5)
        finish_5 = False
        while True:
            per_core_cpu_util = psutil.cpu_percent(interval=None, percpu=True)
            mc_prc_cpu_util = self.memcached.get_cpu_percent()
            print("per core:", per_core_cpu_util)
            print("memcached:", mc_prc_cpu_util)

            mc_cpu_util = per_core_cpu_util[0]
            if self.memcached.cpu == 2:
                mc_cpu_util += per_core_cpu_util[1]
            print("mc cpu util:", mc_cpu_util)

            if mc_prc_cpu_util <= 70:
                self.memcached.set_cpu(1)
                self.scheduler.update_one(4, False)
            else:
                self.scheduler.update_one(4, True)
                self.memcached.set_cpu(2)
            finish_5 = finish_5 or self.scheduler.is_finished(5)
            if finish_5 and self.scheduler.is_finished(4):
                self.scheduler.remove_all_containers()
                self.memcached.set_cpu(2)
                self.timer.destroy_timer()
                break
            time.sleep(0.5)

    def periodic_scheduler(self):
        while True:
            # https://psutil.readthedocs.io/en/latest/#psutil.cpu_percent
            per_core_cpu_util = psutil.cpu_percent(interval=None, percpu=True)
            mc_prc_cpu_util = self.memcached.get_cpu_percent()
            print("per core:", per_core_cpu_util)
            print("memcached:", mc_prc_cpu_util)

            mc_cpu_util = per_core_cpu_util[0]
            if self.memcached.cpu == 2:
                mc_cpu_util += per_core_cpu_util[1]
            print("mc cpu util:", mc_cpu_util)

            # set memcached cpu affinity
            if mc_cpu_util <= 70:
                self.memcached.set_cpu(1)
                # update container
                self.scheduler.update_queue(add=True)
                # self.scheduler.update_group("0", "1,")
            else:
                # update container
                self.scheduler.update_queue(add=False)
                # self.scheduler.update_group("0")
                self.memcached.set_cpu(2)

            self.scheduler.clean_up_batches()

            if self.scheduler.all_done():
                print("All jobs done")
                self.scheduler.remove_all_containers()
                self.memcached.set_cpu(2)
                self.timer.destroy_timer()
                break

            time.sleep(1)

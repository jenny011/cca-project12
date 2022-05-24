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
        # print(self.memcached)
        self.scheduler = Scheduler(self.timer, jobs_config, groups_config)
        self.scheduler.print_containers()

    def start_jobs(self):
        for i in range(2):
            # print("Starting group", str(i))
            self.scheduler.start_group(str(i))

    def new_periodic_scheduler(self):

        # run ferret
        print("<===============FFT===============>")
        self.scheduler.start_one(4)
        print("<===============Ferret===============>")
        self.scheduler.start_one(0)
        while True:
            per_core_cpu_util = psutil.cpu_percent(interval=None, percpu=True)
            mc_prc_cpu_util = self.memcached.get_cpu_percent()
            print("per core:", per_core_cpu_util)
            print("memcached:", mc_prc_cpu_util)

            # mc_cpu_util = per_core_cpu_util[0]
            # if self.memcached.cpu == 2:
            #     mc_cpu_util += per_core_cpu_util[1]
            # print("mc cpu util:", mc_cpu_util)
            if mc_prc_cpu_util <= 50:
                self.scheduler.unpause_one(4)
            else:
                self.scheduler.pause_one(4)

            if mc_prc_cpu_util <= 70:
                self.memcached.set_cpu(1)
                self.scheduler.update_one(0, "1,2,3")
            else:
                self.scheduler.update_one(0, "2,3")
                self.memcached.set_cpu(2)

            fft_finished = self.scheduler.is_finished(4)
            if self.scheduler.is_finished(0):
                break
            time.sleep(0.5)

        # run freqmine and dedup
        print("<===============Freqmine===============>")
        print("<===============Canneal===============>")
        self.scheduler.start_one(1)
        self.scheduler.start_one(2)
        while True:
            per_core_cpu_util = psutil.cpu_percent(interval=None, percpu=True)
            mc_prc_cpu_util = self.memcached.get_cpu_percent()
            print("per core:", per_core_cpu_util)
            print("memcached:", mc_prc_cpu_util)

            # mc_cpu_util = per_core_cpu_util[0]
            # if self.memcached.cpu == 2:
            #     mc_cpu_util += per_core_cpu_util[1]
            # print("mc cpu util:", mc_cpu_util)
            if mc_prc_cpu_util <= 50:
                self.scheduler.unpause_one(4)
            else:
                self.scheduler.pause_one(4)

            if mc_prc_cpu_util <= 70:
                self.memcached.set_cpu(1)
                self.scheduler.update_one(1, "1,2,3")
                self.scheduler.update_one(2, "2,3")
            else:
                self.scheduler.update_one(1, "2,3")
                self.scheduler.update_one(2, "2")
                self.memcached.set_cpu(2)
            freqmine_finished = self.scheduler.is_finished(1)
            canneal_finished = self.scheduler.is_finished(2)
            fft_finished = self.scheduler.is_finished(4)
            if freqmine_finished and canneal_finished:
                break
            time.sleep(0.5)

        # run canneal and fft
        print("<===============Blackscholes===============>")
        print("<===============Dedup===============>")
        self.scheduler.start_one(3)
        self.scheduler.start_one(5)
        while True:
            per_core_cpu_util = psutil.cpu_percent(interval=None, percpu=True)
            mc_prc_cpu_util = self.memcached.get_cpu_percent()
            print("per core:", per_core_cpu_util)
            print("memcached:", mc_prc_cpu_util)

            # mc_cpu_util = per_core_cpu_util[0]
            # if self.memcached.cpu == 2:
            #     mc_cpu_util += per_core_cpu_util[1]
            # print("mc cpu util:", mc_cpu_util)
            if mc_prc_cpu_util <= 50:
                self.scheduler.unpause_one(4)
            else:
                self.scheduler.pause_one(4)

            if mc_prc_cpu_util <= 70:
                self.memcached.set_cpu(1)
                self.scheduler.update_one(3, "1,2,3")
            else:
                self.scheduler.update_one(3, "2,3")
                self.memcached.set_cpu(2)
            blackscholes_finished = self.scheduler.is_finished(3)
            dedup_finished = self.scheduler.is_finished(5)
            fft_finished = self.scheduler.is_finished(4)
            if blackscholes_finished and dedup_finished:
                break
            time.sleep(0.5)

        self.scheduler.unpause_one(4)
        self.scheduler.update_one(4, "2,3")
        while True:
            fft_finished = self.scheduler.is_finished(4)
            if fft_finished:
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

            time.sleep(0.5)
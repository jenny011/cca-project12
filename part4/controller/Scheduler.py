import os, sys, json
from Container import *

class Scheduler():
    def __init__(self, timer, jobs_config, groups_config):
        self.ci = ContainerInterface(timer)
        self.groups = {}
        # original cpuset
        self.group_cpu = {}
        self.queue = []

        with open(jobs_config, "r") as jobs_f:
            jobs = json.load(jobs_f)
        with open(groups_config, "r") as groups_f:
            groups = json.load(groups_f)

        # populate self.groups and self.group_cpu
        for gid, names in groups.items():
            self.groups[gid] = []
            for name in names:
                self.groups[gid].append(self.ci.create_container(jobs[name]))
            self.group_cpu[gid] = jobs[self.groups[gid][0].name]["cpuset_cpus"]

        for gid, cpu in self.group_cpu.items():
            print(gid, cpu)

        # populate self.queue
        # for names in [["ferret"], ["freqmine"], ["canneal", "blackscholes"], ["dedup", "fft"]]:
        #     batch = []
        #     for name in names:
        #         for gid, containers in self.groups.items():
        #             for container in containers:
        #                 if container.name == name:
        #                     batch.append({"container":container,"cpus":self.group_cpu[gid]})
        #     self.queue.append(batch)
        # priority list(based on time it takes to finish the job)
        self.priority = []
        self.collocate = []
        self.collocate_id = 0
        for name in ["ferret", "freqmine", "canneal", "blackscholes"]:
            for gid, containers in self.groups.items():
                for container in containers:
                    if container.name == name:
                        self.priority.append({"container":container, "cpus": self.group_cpu[gid], "act_cpus": self.group_cpu[gid]} )
        for name in ["dedup", "fft"]:
            for gid, containers in self.groups.items():
                for container in containers:
                    if container.name == name:
                        self.collocate.append({"container":container, "cpus": self.group_cpu[gid], "act_cpus": self.group_cpu[gid]} )
        self.running = {"ferret":False, "freqmine":False, "canneal":False, "blackscholes":False, "fft":False, "dedup":False}


    def start_group(self, gid):
        for container in self.groups[gid]:
            self.ci.start_container(container)

    def pause_group(self, gid):
        for container in self.groups[gid]:
            self.ci.pause_container(container)

    def unpause_group(self, gid):
        for container in self.groups[gid]:
            self.ci.unpause_container(container)

    def stop_group(self, gid):
        for container in self.groups[gid]:
            self.ci.stop_container(container)

    def update_group(self, gid, add_cpus=""):
        # update cpu affinity of group
        # print("group:", self.group_cpu[gid], cpus)
        # print(">>> Update group", gid, "to cpu list", add_cpus+self.group_cpu[gid])
        for container in self.groups[gid]:
            self.ci.update_container(container, add_cpus+self.group_cpu[gid])

    def update_queue(self, add):
        # update cpu affinity of first batch in queue

        # schedule the first non-empty batch
        # Try keep an attr called self.queue_index and update it when you clean_up_batches to the first non-empty batch
        # so that you don't need the while loop
        i = 0
        while len(self.queue[i]) == 0:
            i+=1

        # give more cpu
        if add:
            for job in self.queue[i]:
                # print(">>> Update queue", job["container"].name, "to cpu list", "1,"+job["cpus"])
                self.ci.update_container(job["container"], "1,"+job["cpus"])
        # revoke cpu
        else:
            for job in self.queue[i]:
                # print(">>> Update queue", job["container"].name, "to cpu list", job["cpus"])
                self.ci.update_container(job["container"], job["cpus"])

    def remove_all_containers(self):
        for k,v in self.groups.items():
            for container in v:
                self.ci.remove_container(container)

    # remove exited jobs from queue-batch
    def clean_up_batches(self):
        for i in range(len(self.queue)):
            for j in range(len(self.queue[i])):
                if self.ci.is_exited(self.queue[i][j]["container"]):
                    del self.queue[i][j]

    def group_done(self, gid):
        for container in self.groups[gid]:
            if not self.ci.is_exited(container):
                return False
        return True

    def all_done(self):
        for gid in self.groups.keys():
            if not self.group_done(gid):
                return False
        return True

    def print_containers(self):
        print("-------groups-------")
        for k,v in self.groups.items():
            print(f"group{k}: ", end="")
            for container in v:
                print(container.name, end="")
            print("\n")

    def start_one(self, idx, colloc=False):
        if colloc and self.collocate_id < len(self.collocate):
            print(f"<==============={self.collocate[self.collocate_id]['container'].name}===============>")
            self.ci.start_container(self.collocate[self.collocate_id]["container"])
            self.running[self.collocate[self.collocate_id]["container"]] = True
        else:
            self.ci.start_container(self.priority[idx]["container"])
            self.running[self.priority[idx]["container"]] = True

    def update_one(self, idx, cpu, colloc=False):
        if colloc:
            if self.collocate_id < len(self.collocate) and cpu != self.collocate[self.collocate_id]["act_cpus"]:
                self.ci.update_container(self.collocate[self.collocate_id]["container"], cpu)
                self.collocate[self.collocate_id]["act_cpus"] = cpu
        else:
            if cpu != self.priority[idx]["act_cpus"]:
                self.ci.update_container(self.priority[idx]["container"], cpu)
                self.priority[idx]["act_cpus"] = cpu

    def pause_one(self):
        if not self.is_finished(0,True):
            if self.collocate_id < len(self.collocate) and self.running[self.collocate[self.collocate_id]["container"].name]:
                self.ci.pause_container(self.collocate[self.collocate_id]["container"])
                self.running[self.collocate[self.collocate_id]["container"].name] = False

    def unpause_one(self):
        if not self.is_finished(0,True):
            if self.collocate_id < len(self.collocate) and not self.running[self.collocate[self.collocate_id]["container"].name]:
                self.ci.unpause_container(self.collocate[self.collocate_id]["container"])
                self.running[self.collocate[self.collocate_id]["container"].name] = True

    def is_finished(self, idx, colloc=False):
        if colloc and self.collocate_id < len(self.collocate):
            exited = self.ci.is_exited(self.collocate[self.collocate_id]["container"])
            if exited:
                self.collocate_id += 1
                print(len(self.collocate), self.collocate_id)
            return exited
        else:
            return self.ci.is_exited(self.priority[idx]["container"])

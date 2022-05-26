import os, sys, json
import docker


class ContainerInterface():
    def __init__(self, timer=None):
        self.client = docker.from_env()
        self.timer = timer

    def list_containers(self, job_names):
        for name in job_names:
            container = self.client.containers.get(name)
            print(f"{container.name}: {container.status}")

    def create_container(self, job):
        # create container with image
        try:
            container = self.client.containers.get(job["name"])
        except:
            print("Create container:", job["name"])
            container = self.client.containers.create(
                name=job["name"],
                image=job["image"],
                command=job["command"],
                cpuset_cpus=job["cpuset_cpus"],
                auto_remove=False, detach=True
            )
        # get latest container config + status
        container.reload()
        self.timer.record_job(job["name"], "create")
        return container

    def start_container(self, container):
        container.reload()
        if container.status == "created":
            container.start()
            self.timer.record_job(container.name, "start")

    def pause_container(self, container):
        container.reload()
        if container.status == "running":
            container.pause()
            print("pause", container.name)
            self.timer.record_job(container.name, "pause")

    def unpause_container(self, container):
        container.reload()
        if container.status == "paused":
            container.unpause()
            print("unpause", container.name)
            self.timer.record_job(container.name, "unpause")

    def stop_container(self, container):
        container.reload()
        if container.status != "exited":
            container.stop()
            self.timer.record_job(container.name, "stop")

    def remove_container(self, container):
        container.reload()
        self.stop_container(container)
        container.remove()

    def update_container(self, container, cpus, mem=None):
        container.reload()
        if container.status != "exited":
            container.update(cpuset_cpus=cpus)
            self.timer.record_job(container.name, "update", "-".join(cpus.split(",")))

    def is_exited(self,container):
        ret = (container.status == "exited")
        if not ret:
            container.reload()
            ret = (container.status == "exited")
            if ret:
                self.timer.record_job(container.name, "exit")
        return ret

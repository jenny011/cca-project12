import os, sys, json
import docker


class ContainerInterface():
    def __init__(self):
        self.client = docker.from_env()

    def list_images(self):
        for image in self.client.images.list("anakli/parsec"):
            print(f"{image.tags}: {image.short_id}")

    def pull_images(self, jobs):
        for job in jobs:
            print("Pulling image:", job["image"])
            image = self.client.images.pull(job["image"])
            print("Pulled:", image.tags)

    def list_containers(self, job_names):
        for name in job_names:
            container = self.client.containers.get(name)
            print(f"{container.name}: {container.status}")

    def create_container(self, job):
        try:
            # update container attrs if container exists
            container = self.client.containers.get(job["name"])
            print("Updating container:", container.name)
            container.reload()
        except docker.errors.NotFound:
            # create container with image
            print("Creating container for:", job["image"])
            container = self.client.containers.create(name=job["name"], image=job["image"], command=job["command"], cpuset_cpus=job["cpuset_cpus"], auto_remove=False, detach=True)
            print("Container created:", container.name)
        self.timer.record_job(job["name"], "create")

    def start_container(self, name):
        container = self.client.containers.get(name)
        if (container.status == "exited"):
            container.start(name)
            self.timer.record_job(name, "start")

    def pause_container(self, name):
        container = self.client.containers.get(name)
        if (container.status == "running"):
            container.pause()
            self.timer.record_job(name, "pause")

    def unpause_container(self, name):
        container = self.client.containers.get(name)
        if (container.status == "paused"):
            container.unpause()
            self.timer.record_job(name, "unpause")

    def stop_container(self, name):
        container = self.client.containers.get(name)
        if (container.status != "exited"):
            container.stop()
            self.timer.record_job(name, "stop")

    def remove_container(self, name):
        container = self.client.containers.get(name)
        self.stop_container(name)
        container.remove()

    def update_container(self, name, cpus, mem=None):
        container = self.client.containers.get(name)
        #mem_limit
        container.update(cpuset_cpus=cpus)
        self.timer.record_job(name, "update", "-".join(cpus.split(",")))

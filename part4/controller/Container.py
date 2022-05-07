import os, sys, json
import docker

# client.containers.run('alpine')
# container.pause()
# container.unpause()
# container.update(cpuset_cpus="0")

# print(container.logs())

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

    def create_containers(self, jobs):
        for job in jobs:
            try:
                # update container attrs if container exists
                container = self.client.containers.get(job["name"])
                print("Updating container:", container.name)
                container.reload()
            except docker.errors.NotFound:
                # pull image if image doesn't exist
                try:
                    image = self.client.images.get(job["image"])
                    print("Image exists:", image.tags)
                except docker.errors.ImageNotFound:
                    print("Pulling image:", job["image"])
                    image = self.client.images.pull(job["image"])
                    print("Pulled:", image.tags)
                # create container with image
                print("Creating container for:", job["image"])
                container = self.client.containers.create(name=job["name"], image=job["image"], command=job["command"], cpuset_cpus=job["cpuset_cpus"], auto_remove=False, detach=True)
                print("Container created:", container.name)

    def start_container(self, name):
        container = self.client.containers.get(name)
        if (container.status == "exited"):
            container.start(name)

    def pause_container(self, name):
        container = self.client.containers.get(name)
        if (container.status == "running"):
            container.pause()

    def unpause_container(self, name):
        container = self.client.containers.get(name)
        if (container.status == "paused"):
            container.unpause()

    def stop_container(self, name):
        container = self.client.containers.get(name)
        if (container.status != "exited"):
            container.stop()

    def remove_container(self, name):
        container = self.client.containers.get(name)
        self.stop_container(name)
        container.remove(cpuset_cpus=cpus)

    def unpdate_container(self, name, cpus, mem=None):
        container = self.client.containers.get(name)
        #mem_limit
        container.update(cpuset_cpus=cpus)

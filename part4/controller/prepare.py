import os, sys, json
from Container import *

def list_images(self):
    for image in self.client.images.list("anakli/parsec"):
        print(f"{image.tags}: {image.short_id}")

def pull_images(self, jobs):
    for job in jobs:
        print("Pulling image:", job["image"])
        image = self.client.images.pull(job["image"])
        print("Pulled:", image.tags)

if __name__ == "__main__":
    env = docker.from_env()
    with open("containers.json", "r") as config:
        containers = json.load(config)
    for job in containers.values():
        print("Pulling image:", job["image"])
        image = env.images.pull(job["image"])
        print("Pulled:", image.tags)
    # pull_images(containers.values())

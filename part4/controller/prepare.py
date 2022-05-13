import os, sys, json
import time
from Container import *

if __name__ == "__main__":
    container = ContainerInterface()

    with open(config_file, "r") as config:
        containers = json.load(config)

    container.pull_images(containers.values())

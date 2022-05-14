import os, sys, json
from datetime import datetime
from Controller import *


if __name__ == "__main__":
    now = datetime.now()
    expnum = now.strftime("%m_%d_%H_%M_%S")
    controller = Controller(expnum,"containers.json", "groups.json")

    controller.start_jobs()
    controller.periodic_scheduler()

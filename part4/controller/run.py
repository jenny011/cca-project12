import os, sys, json
import time
from datetime import datetime
from Controller import *


if __name__ == "__main__":
    now = datetime.now()
    expnum = now.strftime("%m_%d_%H_%M")
    controller = Controller(expnum,"containers.json", "groups.json")
    controller.print_scheduler()
    controller.print_memcached()

    controller.start_jobs()
    while True:
        controller.periodic_scheduler()
        # sleep 1 s
        time.sleep(1)

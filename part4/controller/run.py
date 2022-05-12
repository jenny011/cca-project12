import os, sys, json
import time
from Controller import *

if __name__ == "__main__":
    controller = Controller()
    controller.init_memcached()
    controller.init_scheduler("containers.json", "groups.json")
    controller.print_scheduler()
    controller.print_memcached()

    while True:
        controller.periodic_scheduler()
        # sleep 1 s
        time.sleep(1)

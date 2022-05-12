import os, sys, json
import psutil
import time

data={"time":[], "cpu":[]}
print(time.time())
for i in range(200):
	data["time"].append(time.time())
    data["cpu"].append(psutil.cpu_percent(interval=None, percpu=True))
    time.sleep(1)
print(time.time())
print(data)

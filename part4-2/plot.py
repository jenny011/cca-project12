from sqlite3 import Timestamp
import matplotlib as plt
from asyncio.base_futures import _FINISHED
from datetime import datetime
import os
from re import X
import string
from time import time
from typing import ItemsView
from xml.etree.ElementTree import tostring
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
from matplotlib.ticker import FuncFormatter
from pyparsing import line


import os, argparse, sys


parser = argparse.ArgumentParser(description='argparse')
parser.add_argument('--datadir', '-d', help='data directory', required=True)
args = parser.parse_args()

DATADIR = args.datadir


# set the files 
memcached_file = os.path.join(DATADIR, 'memcached.csv')
latency_file = os.path.join(DATADIR, 'latency.txt')
jobs_file = os.path.join(DATADIR, 'jobs.csv')
controller_file = os.path.join(DATADIR, 'controller.csv')

###### 1.read in data from files ######
 
# read QPS and latency data
def read_mc_data(memcached_file):
    L = []
    with open(memcached_file, 'r') as file:
        line = file.readline()
        while line:
            #print(line)
            line = line.split()
            L.append(line)
            line = file.readline()
    #L[8:188] only keep the data part
    data = pd.DataFrame(L[8:188], index=None, columns=None, dtype=None, copy=None)
    return data

def extract_p95_latency(data):
    p95 = list(data[12])
    p95.pop(0)
    for i in range(len(p95)):
        # convert unit to ms
        p95[i] = float(p95[i])/1000
    return p95

def extract_QPS(data):
    QPS = list(data[16])
    QPS.pop(0)
    for i in range(len(QPS)):
        QPS[i] = float(QPS[i])
        if QPS[i] < 30000:
            print("!!!lower than 30K:", QPS[i])
    return QPS

# read memcached time
def read_controller_time(controller_file):
    with open (controller_file) as file:
        line1 = file.readline()
        crl_start_time = float(line1.split(',')[1])
        line2 = file.readline()
        crl_end_time = float(line2.split(',')[1])
    return crl_start_time, crl_end_time


crl_start, crl_end = read_controller_time(controller_file)
x_length = crl_end - crl_start

# read jobs time
def read_jobs_time(jobs_file, shift):
    jobs_time = {'dedup':[], 'freqmine':[], 'fft':[], 'ferret':[], 'canneal':[], 'blackscholes':[]}
    start_flag = ['start', 'unpause']
    end_flag = ['exit', 'pause']
    stack = [] # help match each job's begin time and end/pause time
    with open(jobs_file) as file:
        line = file.readline() 
        while line:
            #print(shift)
            job, timestamp, operation = line.split(',')[0], float(line.split(',')[1]) - shift, line.split(',')[2]
            #print(job, timestamp, operation)
            if operation in start_flag:
                stack.append([job, timestamp])
            elif operation in end_flag:
                for item in stack:
                    if item[0] == job:
                        jobs_time[job].append([item[1], timestamp])
                        stack.remove(item)
                        break
                        
            line = file.readline()
        return jobs_time

# print(read_jobs_time(jobs_file))

# read memcached CPU
def read_cpu_change(memcached_file):
    mem_cpu = []
    with open (memcached_file) as file:
        line = file.readline()
        while line:
            change_time, cpu_num = float(line.split(',')[0]), float(line.split(',')[1])
            mem_cpu.append([change_time, cpu_num])
            line = file.readline()
    return mem_cpu


#print(read_cpu_change(memcached_file))

###### 2. subplot_a: plot QPS and latency  ######
def plot_latency(axA_95p):
    axA_95p.set_title("QPS and Latency")
    axA_95p.set_xlim([0, 16])
    axA_95p.set_xlabel("Time/s")
    axA_95p.set_xticks(range(0, int(x_length) + 1, 100))
    axA_95p.grid(True)
    axA_95p.set_ylabel("95th percentile latency [ms]")
    axA_95p.tick_params(axis='y', labelcolor='tab:blue')
    # axA_95p.set_ylim([0, 3.2])
    # axA_95p.set_yticks(np.arange(0, 3.2, 0.4))
    axA_95p.set_ylim([0, 0.6])
    axA_95p.set_yticks(np.arange(0, 0.6, 0.1))

def plot_qps(axA_QPS):
    axA_QPS.set_ylabel("Queries Per Second")
    axA_QPS.set_ylim([0, 100000])
    axA_QPS.set_yticks(np.arange(0, 100001, 5000))
    axA_QPS.yaxis.set_major_formatter(
        FuncFormatter(lambda x_val, tick_pos: "{:.0f}k".format(x_val / 1000)))
    axA_QPS.tick_params(axis='y', labelcolor='tab:red')
    axA_QPS.grid(True)

###### 3. subplot_b: jobs time  ######



def plot_jobs(ax_events, jobs_time):
    workloads = ['dedup', 'canneal', 'fft', 'blackscholes', 'ferret', 'freqmine']

    ax_events.set_title("Timeline of PARSEC Jobs")
    ax_events.set_yticks(range(6))
    ax_events.set_yticklabels(workloads)
    ax_events.set_ylim([-1, 6])
    ax_events.set_xlim([0, x_length + 1])
    ax_events.set_xlabel('time [s]')
    ax_events.set_xticks(range(0, int(x_length) + 1, 100))
    ax_events.grid(True)

    print(jobs_time)
    for idx, name in enumerate(workloads):
        color = f'C{idx}'
        for record in jobs_time[name]:
            print(record)
            ax_events.plot(record,[idx, idx], color=color, linewidth=2.5)
            ax_events.scatter(record[0], [idx], c=color, marker='o')
            ax_events.scatter(record[1], [idx], c=color, marker='x')
    plt.show()

###### 4. subplot_c: memcached cpu change  ######
def plot_cpu_num(mem_cpu):
    pass

# crl_start, crl_end = read_controller_time(controller_file)
# jobs_time = read_jobs_time(jobs_file, crl_start)
# data = read_mc_data
# QPS = extract_QPS(data)
# p95 = extract_p95_latency(data)


if __name__ == "__main__":

    # data #
    # data = read_mc_data(memcached_file)
    # # print(data)
    # p95 = extract_p95_latency(data)
    # # print(p95)
    # QPS = extract_QPS(data)
    # # print(QPS)
    # # used time instead of numbers
    # x_label = [i*20 for i in range(len(QPS))]

    controller_s, controller_e = read_controller_time(controller_file)
    jobs_time = read_jobs_time(jobs_file, controller_s)

    fig = plt.figure(figsize=(8, 5))
    fig.suptitle("test")
    ax_events = fig.subplots()

    plot_jobs(ax_events, jobs_time)

    plt.plot()
    plt.show()




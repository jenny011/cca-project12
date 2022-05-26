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
    count = 0
    for i in range(len(p95)):
        # convert unit to ms
        p95[i] = float(p95[i])/1000
        if p95[i] > 1.5:
            print("SLO Violation:", p95[i])
            count += 1
    print("SLO Violation Ratio:", count / len(p95))

    return p95

def extract_QPS(data):
    QPS = list(data[16])
    QPS.pop(0)
    for i in range(len(QPS)):
        QPS[i] = float(QPS[i])
        # if QPS[i] < 30000:
        #     print("!!!lower than 30K:", QPS[i])
    return QPS

# read memcached time
def read_controller_time(controller_file):
    with open (controller_file) as file:
        line1 = file.readline()
        crl_start_time = float(line1.split(',')[1])
        line2 = file.readline()
        crl_end_time = float(line2.split(',')[1])
    return crl_start_time, crl_end_time

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
# return x-time, y-cpu
def read_cpu_change(memcached_file, shift):
    mem_cpu = [[],[]]
    prev_time = -1
    prev_cpu = 0
    final_time = -1
    with open (memcached_file) as file:
        line = file.readline()
        while line:
            change_time, cpu_num = float(line.split(',')[0]), float(line.split(',')[1])
            if prev_time != -1:
                if cpu_num != prev_cpu:
                    mem_cpu[0].append([prev_time+2, change_time - shift-2])
                    mem_cpu[1].append([prev_cpu, prev_cpu])
                    prev_time = change_time - shift
                    prev_cpu = cpu_num
            else :
                prev_time = change_time - shift
                prev_cpu = cpu_num
            final_time = change_time - shift
            line = file.readline()
        mem_cpu[0].append([prev_time+2, final_time-2])
        mem_cpu[1].append([prev_cpu, prev_cpu])
    return mem_cpu


#print(read_cpu_change(memcached_file))

###### 2. subplot_a: plot QPS and latency  ######
def plot_latency(axA_95p):
    axA_95p.set_title("QPS and Latency")
    axA_95p.set_xlim([0, 16])
    axA_95p.set_xlabel("Time [s]")
    axA_95p.set_xticks(range(0, int(x_length) + 1, 100))
    axA_95p.grid(True)
    axA_95p.set_ylabel("95th percentile latency [ms]")
    axA_95p.tick_params(axis='y', labelcolor='tab:blue')
    # axA_95p.set_ylim([0, 3.2])
    # axA_95p.set_yticks(np.arange(0, 3.2, 0.4))
    axA_95p.set_ylim([0, 3])
    axA_95p.set_yticks(np.arange(0, 3, 0.3))

def plot_qps(axA_QPS):
    axA_QPS.set_ylabel("Queries Per Second")
    axA_QPS.set_ylim([0, 100000])
    axA_QPS.set_yticks(np.arange(0, 100001, 10000))
    axA_QPS.yaxis.set_major_formatter(
        FuncFormatter(lambda x_val, tick_pos: "{:.0f}k".format(x_val / 1000)))
    axA_QPS.tick_params(axis='y', labelcolor='tab:red')

###### 3. subplot_b: jobs time  ######
def plot_mc(axB_mc):
    axB_mc.set_title("Memcached CPU")
    axB_mc.set_xlim([0, 16])
    axB_mc.set_xlabel("Time [s]")
    axB_mc.set_xticks(range(0, int(x_length) + 1, 100))
    axB_mc.grid(True)
    axB_mc.set_ylabel("CPU number")
    axB_mc.tick_params(axis='y', labelcolor='tab:blue')
    # axA_95p.set_ylim([0, 3.2])
    # axA_95p.set_yticks(np.arange(0, 3.2, 0.4))
    axB_mc.set_ylim([0, 4.5])
    axB_mc.set_yticks(np.arange(1, 4.5, 1))



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

    for idx, name in enumerate(workloads):
        color = f'C{idx}'
        for record in jobs_time[name]:
            ax_events.plot(record,[idx, idx], color=color, linewidth=1.8)
            ax_events.scatter(record[0], [idx], c=color, marker='')
            ax_events.scatter(record[1], [idx], c=color, marker='')

###### 4. subplot_c: memcached cpu change  ######
def plot_cpu_num(mem_cpu):
    pass

# crl_start, crl_end = read_controller_time(controller_file)
# jobs_time = read_jobs_time(jobs_file, crl_start)
# data = read_mc_data
# QPS = extract_QPS(data)
# p95 = extract_p95_latency(data)


if __name__ == "__main__":
    for k in range(1,4):
        memcached_file = os.path.join(DATADIR, str(k), 'memcached.csv')
        latency_file = os.path.join(DATADIR, str(k), 'latency.txt')
        jobs_file = os.path.join(DATADIR, str(k), 'jobs.csv')
        controller_file = os.path.join(DATADIR, str(k), 'controller.csv')

        data = read_mc_data(latency_file)
        p95 = extract_p95_latency(data)
        QPS = extract_QPS(data)
        x_label = [i*10 for i in range(len(QPS))]

        controller_s, controller_e = read_controller_time(controller_file)
        x_length = controller_e - controller_s
        print("Total time:", x_length/60)
        jobs_time = read_jobs_time(jobs_file, controller_s)
        mem_cpu = read_cpu_change(memcached_file, controller_s)

        fig = plt.figure(figsize=(8, 6))
        fig.suptitle(f"{k}A")

        axA_95p, ax_events = fig.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]})
        axA_QPS = axA_95p.twinx()
        plot_latency(axA_95p)
        plot_qps(axA_QPS)
        artistA_95p, = axA_95p.plot(x_label, p95, 'o-', markersize=3.5, linewidth=1.8, color='tab:red')
        axA_95p.plot(x_label, [1.5 for x in x_label], '-', linewidth=1, color='tab:green')
        artistA_QPS, = axA_QPS.plot(x_label, QPS, 'o', markersize=3.5, color='tab:blue')    
        plt.legend([artistA_QPS, artistA_95p], ['QPS', '95th latency'], loc='upper right')
        plot_jobs(ax_events, jobs_time)
        fig.tight_layout()


        fig2 = plt.figure(figsize=(8, 4))
        fig2.suptitle(f"{k}B")

        axB_mc = fig2.subplots()
        axB_QPS = axB_mc.twinx()
        plot_mc(axB_mc)
        plot_qps(axB_QPS)
        artistB_mc, = axB_mc.plot(mem_cpu[0][0],mem_cpu[1][0], '-', color='tab:red', linewidth=2)
        for i in range(1,len(mem_cpu[0])):
            axB_mc.plot(mem_cpu[0][i],mem_cpu[1][i], '-', color='tab:red', linewidth=2)
        # artistB_mc, = axB_mc.plot(mem_cpu[0], mem_cpu[1], '-', color='tab:red')
        artistB_QPS, = axB_QPS.plot(x_label, QPS, 'o', markersize=3, color='tab:blue')
        plt.legend([artistB_mc, artistB_QPS], ['memcached cpu', 'QPS'], loc='upper right')
        plt.subplots_adjust(hspace=0.2, bottom=0.2)
        fig2.tight_layout()

        plt.plot()
        plt.show()




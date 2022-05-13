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


def time_convert(time_string) -> float:
    T = time_string.split(":")
    return (float(T[0])*3600 + float(T[1])*60 + float(T[2]))

    
###### 1. read QPS and latency data ######
def read_mc_data(memcached_file):
    L = []
    with open(memcached_file, 'r') as file:
        line = file.readline()
        while line:
            line = line.split()
            L.append(line)
            line = file.readline()
     
    data = pd.DataFrame(L, index=None, columns=None, dtype=None, copy=None)
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
    #print(QPS)

###### 3. read from json ######

def read_parsec_data(json_file):
    with open (json_file) as f:
        parsec04 = json.load(f)

    running_time = {}
    for i in range(0, 6):
        running_time[parsec04['items'][i]['status']['containerStatuses'][0]['name'].lstrip("-")] = [parsec04['items'][i]['status']['containerStatuses'][0]['state']['terminated']['finishedAt'][-9:-1], 
        parsec04['items'][i]['status']['containerStatuses'][0]['state']['terminated']['startedAt'][-9:-1]]
    time_finished, time_started, time_last = {},{}, {}
    for item in running_time:
        name = item[6:].lstrip("-")
        time_finished[name] = time_convert(running_time[item][0])
        time_started[name] = time_convert(running_time[item][1])   
        time_last[name] = time_convert(running_time[item][0]) - time_convert(running_time[item][1])
    return time_started, time_finished, time_last

def extract_start_finish(time_started, time_finished):
    # print('\n',time_started, '\n', time_finished, '\n', time_last)

    min_finished = time_finished[min(time_finished, key = time_finished.get)]
    # print("min_finished:  ", min_finished)
    min_started = time_started[min(time_started, key = time_started.get)]
    # print("min_started:  ", min_started)
    mini = min(min_finished, min_started)

    max_finished = time_finished[max(time_finished, key = time_finished.get)]
    # print("max_finished:  ", max_finished)
    print("total_time:", max_finished - min_started)

    for item in time_finished:
        time_finished[item] = time_finished[item] - mini

    for item in time_started:
        time_started[item] = time_started[item] - mini

    return time_started, time_finished



###### 2. plot QPS and latency  ######
def plot_latency(axA_95p):
    axA_95p.set_title("QPS and Latency")
    axA_95p.set_xlim([0, 16])
    axA_95p.set_xlabel("timestamp")
    axA_95p.set_xticks(range(0, 300 + 1, 20))
    axA_95p.grid(True)
    axA_95p.set_ylabel("95th percentile latency [ms]")
    axA_95p.tick_params(axis='y', labelcolor='tab:blue')
    # axA_95p.set_ylim([0, 3.2])
    # axA_95p.set_yticks(np.arange(0, 3.2, 0.4))
    axA_95p.set_ylim([0, 0.6])
    axA_95p.set_yticks(np.arange(0, 0.6, 0.1))

def plot_qps(axA_QPS):
    axA_QPS.set_ylabel("Queries Per Second")
    axA_QPS.set_ylim([0, 40000])
    axA_QPS.set_yticks(np.arange(0, 40001, 5000))
    axA_QPS.yaxis.set_major_formatter(
        FuncFormatter(lambda x_val, tick_pos: "{:.0f}k".format(x_val / 1000)))
    axA_QPS.tick_params(axis='y', labelcolor='tab:red')
    axA_QPS.grid(True)

def plot_jobs(ax_events, workloads):
    ax_events.set_title("Timeline of PARSEC Jobs")
    ax_events.set_yticks(range(6))
    ax_events.set_yticklabels(workloads)
    ax_events.set_ylim([-1, 6])
    ax_events.set_xlim([0, 200])
    ax_events.set_xlabel('time [s]')
    ax_events.set_xticks(range(0, 300 + 1, 20))
    ax_events.grid(True)

    for idx, name in enumerate(workloads):
        color = f'C{idx}'
        ax_events.plot([time_started[name], time_finished[name]],[idx, idx], color=color, linewidth=2)
        ax_events.scatter(time_started[name], [idx], c=color, marker='|')
        ax_events.scatter(time_finished[name], [idx], c=color, marker='|')

def annotation_line( ax, xmin, xmax, y, text, ytext=0, linecolor='black', linewidth=1, fontsize=12 ):

    ax.annotate('', xy=(xmin, y), xytext=(xmax, y), xycoords='data', textcoords='data',
            arrowprops={'arrowstyle': '|-|', 'color':linecolor, 'linewidth':linewidth})
    ax.annotate('', xy=(xmin, y), xytext=(xmax, y), xycoords='data', textcoords='data',
            arrowprops={'arrowstyle': '<-', 'color':linecolor, 'linewidth':linewidth})

    xcenter = xmin + (xmax-xmin)/2
    if ytext==0:
        ytext = y + ( ax.get_ylim()[1] - ax.get_ylim()[0] ) / 20

    ax.annotate( text, xy=(xcenter,ytext), ha='center', va='center', color=color, fontsize=fontsize)


if __name__ == "__main__":
    basedir = "part3-exp09"
    num_runs = 3
    for i in range(num_runs):
        memcached_file = f"{basedir}/memcached0{i+1}.txt"
        json_file = f"{basedir}/results0{i+1}.json"
        figure_name = f"Run {i+1}"

        # data #
        data = read_mc_data(memcached_file)
        # print(data)
        p95 = extract_p95_latency(data)
        # print(p95)
        QPS = extract_QPS(data)
        # print(QPS)
        # used time instead of numbers
        x_label = [i*20 for i in range(len(QPS))]
        #print(x_label)

        time_started, time_finished, time_last = read_parsec_data(json_file)
        time_started, time_finished = extract_start_finish(time_started, time_finished)

        fig = plt.figure(figsize=(8, 5))
        fig.suptitle(figure_name)
        # axA_95p, ax_events = fig.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1.5]})
        axA_95p = fig.subplots()
        # axA_QPS = axA_95p.twinx()
        plot_latency(axA_95p)
        # plot_qps(axA_QPS)
        artistA_95p, = axA_95p.plot(x_label, p95, 'o-', color='tab:blue')
        # artistA_QPS, = axA_QPS.plot(x_label, QPS, 'o-', color='tab:red')    
        # plt.legend([artistA_QPS, artistA_95p], ['QPS', '95th latency'], loc='center right')
        axA_95p.legend([artistA_95p], ['95th latency'])
        # plt.subplots_adjust(hspace=0.2, bottom=0.2)
        fig.tight_layout()

        workloads = ['dedup', 'canneal', 'splash2x-fft', 'blackscholes', 'ferret', 'freqmine']
        for idx, name in enumerate(workloads):
            color = f'C{idx}'
            annotation_line( ax=axA_95p, text=name, xmin=time_started[name], xmax=time_finished[name], \
                        y=(idx+1)*0.05, ytext=(idx+1)*0.05 + 0.01, linewidth=1.5, linecolor=color, fontsize=11 )
        # plot_jobs(ax_events,workloads)

        plt.plot()
        plt.savefig(figure_name + ".pdf")
        plt.show()


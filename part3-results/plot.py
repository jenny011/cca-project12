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
    return QPS
    #print(QPS)


###### 2. plot QPS and latency  ######

def config_QPS_ax(ax):
    ax.set_ylabel("Queries per second")
    ax.set_ylim([0, 40000])
    ax.set_yticks(np.arange(0, 40001, 5000))
    ax.yaxis.set_major_formatter(
        FuncFormatter(lambda x_val, tick_pos: "{:.0f}k".format(x_val / 1000)))
    ax.tick_params(axis='y', labelcolor='tab:red')
    ax.grid(True)
    return ax.plot(x_label, QPS, '-x', color='tab:red')

###### 3. read from json ######

def read_parsec_data(json_file):
    with open (json_file) as f:
        parsec04 = json.load(f)

    running_time = {}
    for i in range(0, 6):
        running_time[parsec04['items'][i]['status']['containerStatuses'][0]['name']] = [parsec04['items'][i]['status']['containerStatuses'][0]['state']['terminated']['finishedAt'][-9:-1], 
        parsec04['items'][i]['status']['containerStatuses'][0]['state']['terminated']['startedAt'][-9:-1]]
    time_finished, time_started, time_last = {},{}, {}
    for item in running_time:
        time_finished[item[6:]] = time_convert(running_time[item][0])
        time_started[item[6:]] = time_convert(running_time[item][1])   
        time_last[item[6:]] = time_convert(running_time[item][0]) - time_convert(running_time[item][1])


    print('\n',time_started, '\n', time_finished, '\n', time_last)


if __name__ == "__main__":
    num_runs = 3
    for i in range(num_runs):
        memcached_file = "memcached0{0}.txt".format(i+1)
        json_file = "results{0}.json".format(i+1)
        figure_name = "Run {0}".format(i+1)

        data = read_mc_data(memcached_file)
        print(data)
        p95 = extract_p95_latency(data)
        print(p95)
        QPS = extract_QPS(data)
        # print(QPS)
        # used time instead of numbers
        x_label = [i for i in range(len(QPS))]
        #print(x_label)

        fig = plt.figure(figsize=(8, 5))
        axA_95p, ax_events = fig.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1.5]})

        fig.suptitle(figure_name)
        axA_95p.set_title("QPS and latency")
        axA_95p.set_xlim([0, 16])
        axA_95p.set_xlabel("Timestamp")
        axA_95p.set_xticks(range(0, 17, 1))
        axA_95p.grid(True)
        axA_95p.set_ylabel("95th Latency / ms")
        axA_95p.tick_params(axis='y', labelcolor='tab:blue')
        axA_95p.set_ylim([0, 3.2])
        axA_95p.set_yticks(np.arange(0, 3.2, 0.4))

        artistA_95p, = axA_95p.plot(x_label, p95, 'o-', color='tab:blue')
        axA_QPS = axA_95p.twinx()

        ###### QPS #######
        axA_QPS.set_ylabel("Queries per second")
        axA_QPS.set_ylim([0, 40000])
        axA_QPS.set_yticks(np.arange(0, 40001, 5000))
        axA_QPS.yaxis.set_major_formatter(
            FuncFormatter(lambda x_val, tick_pos: "{:.0f}k".format(x_val / 1000)))
        axA_QPS.tick_params(axis='y', labelcolor='tab:red')
        axA_QPS.grid(True)
        artistA_QPS = axA_QPS.scatter(x_label, QPS,  color='tab:red')    


        # artistA_QPS = config_QPS_ax(axA_QPS)
        # axA_QPS.legend([artistA_QPS, artistA_95p], ['QPS', '95th latency'], loc='upper right')
        plt.legend([artistA_QPS, artistA_95p], ['QPS', '95th latency'], loc='center right')

        plt.subplots_adjust(hspace=0.2, bottom=0.2)
        fig.tight_layout()

        ###### 3. read from json ######

        


        min_finished = time_finished[min(time_finished, key = time_finished.get)]
        print("min_finished:  ", min_finished)
        min_started = time_started[min(time_started, key = time_started.get)]
        print("min_started:  ", min_started)
        mini = min(min_finished, min_started)

        max_finished = time_finished[max(time_finished, key = time_finished.get)]
        print("max_finished:  ", max_finished)
        print("total_time:", max_finished - min_started)


        for item in time_finished:
            time_finished[item] = time_finished[item] - mini

        for item in time_started:
            time_started[item] = time_started[item] - mini

        print('\n',time_started, '\n', time_finished, '\n', time_last)

        ###### 4. plot for PARSEC ######

        workloads = ['dedup', 'canneal', '-splash2x-fft', 'blackscholes', 'ferret', 'freqmine']
        ax_events.set_yticks(range(6))
        ax_events.set_yticklabels(workloads)
        ax_events.set_ylim([-1, 6])
        ax_events.set_xlim([0, 200])
        ax_events.set_xlabel('Time / s')
        ax_events.set_xticks(range(0, 360 + 1, 20))
        ax_events.grid(True)

        for idx, name in enumerate(workloads):
            color = f'C{idx}'
            ax_events.plot([time_started[name], time_finished[name]],[idx, idx], color=color, linewidth=2.5)
            ax_events.scatter(time_started[name], [idx], c=color, marker='o')
            ax_events.scatter(time_finished[name], [idx], c=color, marker='x')



        plt.plot()
        plt.savefig(figure_name + ".pdf")
        plt.show()


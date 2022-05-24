from audioop import avg
import numpy as np
import matplotlib.pyplot as plt
import json
from matplotlib.ticker import FuncFormatter

def read_mc(dirname):
    latency = [[] for i in range(3)]
    qps = [[] for i in range(3)]
    start_time = [[] for i in range(3)]
    end_time = [[] for i in range(3)]

    for fi in range(0,3):
        with open(f"{dirname}/perf-0{fi+1}.txt") as fd:
            for i, line in enumerate(fd.readlines()):
                if i >= 1 and i <= 24:
                    latency[fi].append(float(line.split()[-8])/1000)
                    qps[fi].append(float(line.split()[-4]))
                    start_time[fi].append(float(line.split()[-2])/1000)
                    end_time[fi].append(float(line.split()[-1])/1000)


    latency_avg = [np.mean(x) for x in zip(latency[0],latency[1],latency[2])]   
    # # x_std = [np.std(x) for x in zip(xs[0],xs[1],xs[2])]   
    qps_avg = [np.mean(x) for x in zip(qps[0],qps[1],qps[2])]
    # start_time_avg = [np.mean(x) for x in zip(start_time[0],start_time[1],start_time[2])]
    # end_time_avg = [np.mean(x) for x in zip(end_time[0],end_time[1],end_time[2])]
    # y_std = [np.std(y) for y in zip(ys[0],ys[1],ys[2])]
    # return latency_avg, qps_avg, start_time_avg, end_time_avg
    return latency_avg, qps_avg, start_time[0], end_time[0]

def read_cpu(dirname):
    data = []
    for fi in range(0,1):
        with open(f"{dirname}/cpu-0{fi+1}.json") as f:
            data.append(json.load(f))
    return data[0]

def find_time(cpu_time, start_time, end_time):
    indexes = []
    j = 0
    start = 0
    end = 0
    for i in range(len(start_time)):
        while cpu_time[j] < start_time[i] and j < len(cpu_time):
            j+=1
        start = j
        while cpu_time[j] < end_time[i] and j < len(cpu_time):
            j+=1
        end = j
        indexes.append((start, end))
    return indexes

def compute_cpu_util(cpu, indexes, core):
    cpu_util = []
    if core == 1:
        for i in range(len(indexes)):
            u = 0
            minu = core*100
            s, e = indexes[i]
            for j in range(s,e):
                u += cpu[j][0]
                minu = min(minu, cpu[j][0])
            u -= minu
            cpu_util.append(u/(e-s-1))
    else:
        for i in range(len(indexes)):
            u = 0
            minu = core*100
            s, e = indexes[i]
            for j in range(s,e):
                u += cpu[j][0] + cpu[j][1]
                minu = min(minu, cpu[j][0] + cpu[j][1])
            u -= minu
            cpu_util.append(u/(e-s-1))
    return cpu_util


def plotline(y, x, labelname):
    msize = 6
    m = "o"
    medge = 0.5
    mfill='none'
    mecolor = "w"
    lwidth = 1.5
    plotstyle=''

    plt.plot(x, y,
        fmt=plotstyle, linewidth=lwidth, 
        markersize=msize, marker = m,
        markeredgewidth=medge, markeredgecolor=mecolor,
        capsize=3, capthick=1, label=labelname)


if __name__ == "__main__":
    for core in range(1,3):
        latency, qps, start_time, end_time = read_mc(f"c{core}-t2")
        data = read_cpu(f"c{core}-t2")

        indexes = find_time(data["time"], start_time, end_time)

        cpu_util = compute_cpu_util(data["cpu"], indexes, core)

        fig,ax_mc = plt.subplots()

        ax_mc.set_xlim([0, 120000+5000])
        ax_mc.set_xticks(range(0, 120000+5000, 10000))
        ax_mc.xaxis.set_major_formatter(
            FuncFormatter(lambda x_val, tick_pos: "{:.0f}k".format(x_val / 1000)))
        ax_mc.set_xlabel("QPS")
        ax_mc.set_ylim([-0.1, 2+0.1])
        ax_mc.set_yticks(np.arange(0, 2+0.1, 0.25))
        ax_mc.grid(True)
        ax_mc.set_ylabel("95th percentile latency [ms]")
        ax_mc.tick_params(axis='y', labelcolor='tab:blue')
        # 1.5ms SLO line
        artist_mc, = ax_mc.plot(qps, latency, 'o-', markersize=5, color='tab:blue')
        ax_mc.plot([0, 120000+5000], [1.5,1.5], linestyle='dotted', linewidth=2, color="black")
        plt.annotate('1.5ms latency SLO', xy=(3000,1.55))

        ax_cpu = ax_mc.twinx()
        ax_cpu.set_ylim([-core*100/20, core*100+core*100/20])
        ax_cpu.set_yticks(np.arange(0, core*100+core*100/20, core*12.5))
        # ax_cpu.grid(True)
        ax_cpu.set_ylabel("cpu utilization [%]")
        ax_cpu.tick_params(axis='y', labelcolor='tab:red') 
        artist_cpu, = ax_cpu.plot(qps, cpu_util, 'o-', markersize=5, color='tab:red')

        plt.legend([artist_mc, artist_cpu], ['p95 latency', 'cpu utilization'], loc='upper left')


        if core == 1:
            plt.title(f"2 Threads, 1 Core")
        else:
            plt.title(f"2 Threads, 2 Cores")
        plt.show()


from audioop import avg
import numpy as np
import matplotlib.pyplot as plt
import csv

def read(dirname):
    xs = [[] for i in range(3)]
    ys = [[] for i in range(3)]

    for fi in range(0,3):
        with open(f"{dirname}/0{fi+1}.txt") as fd:
            for i, line in enumerate(fd.readlines()):
                if i >= 1 and i <= 24:
                    ys[fi].append(float(line.split()[-8])/1000)
                    xs[fi].append(float(line.split()[-4]))

    x_avg = [np.mean(x) for x in zip(xs[0],xs[1],xs[2])]   
    x_std = [np.std(x) for x in zip(xs[0],xs[1],xs[2])]   
    y_avg = [sum(y)/3 for y in zip(ys[0],ys[1],ys[2])]
    y_std = [np.std(y) for y in zip(ys[0],ys[1],ys[2])]
    return y_avg, y_std, x_avg, x_std


def plotline(y, yerr, x, xerr, labelname):
    msize = 6
    m = "o"
    medge = 0.5
    mfill='none'
    mecolor = "w"
    lwidth = 1.5
    plotstyle=''

    plt.errorbar(x, y, xerr=xerr, yerr=yerr,
        fmt=plotstyle, linewidth=lwidth, 
        markersize=msize, marker = m,
        markeredgewidth=medge, markeredgecolor=mecolor,
        capsize=3, capthick=1, label=labelname)


if __name__ == "__main__":
    c1t1y_avg, c1t1y_std, c1t1x_avg, c1t1x_std = read("c1-t1")
    c2t1y_avg, c2t1y_std, c2t1x_avg, c2t1x_std = read("c2-t1")
    c1t2y_avg, c1t2y_std, c1t2x_avg, c1t2x_std = read("c1-t2")
    c2t2y_avg, c2t2y_std, c2t2x_avg, c2t2x_std = read("c2-t2")

    fig = plt.figure()
    plotline(c1t1y_avg, c1t1y_std, c1t1x_avg, c1t1x_std, "1 threads, 1 core")
    plotline(c2t1y_avg, c2t1y_std, c2t1x_avg, c2t1x_std, "1 threads, 2 core")
    plotline(c1t2y_avg, c1t2y_std, c1t2x_avg, c1t2x_std, "2 threads, 1 core")
    plotline(c2t2y_avg, c2t2y_std, c2t2x_avg, c2t2x_std, "2 threads, 2 core")

    plt.title("4.1.a: Memcached Performance")
    plt.xlabel("QPS [queries per second]")
    plt.ylabel("95th percentile latency [ms]")

    plt.xticks([x for x in range(0, 125000, 10000)], [f"{x}k" for x in range(0, 125, 10)])

    plt.legend(title='number of threads and cores', loc='upper left')

    ax = plt.gca()
    ax.set_facecolor('#EDECEF')
    plt.grid()
    plt.show()


import numpy as np
import csv
import matplotlib.pyplot as plt

def read(filename):
    i=0
    output = []
    with open(filename, "r") as f:
        preader = csv.reader(f, delimiter=",")
        for row in preader:
            if i != 0 and i != 6:
                for j in range(1,len(row)):
                    if row[j]:
                        row[j] = float(row[j])
                for j in range(2,len(row)):
                    row[j] = row[1]/row[j]
                row[1] = 1
                output.append(row[1:])
            i += 1
    return output

msize = 7
m = "o"
medge = 1
mfill='none'
mecolor = "w"
lwidth = 1.2
plotstyle=''

def plotline(x, y, labelname):
    plt.plot(x, y, linewidth=lwidth, markersize=msize,marker = m,markeredgewidth=medge,markeredgecolor=mecolor,label=labelname)

if __name__ == "__main__":
    data = read("./part2b-sec.csv")
    x = [1, 3, 6, 12]
    label = ["dedup", "blackscholes", "ferret", "freqmine", "canneal"]

    fig = plt.figure()
    for i in range(5):
        plotline(x, data[i],label[i])
    plt.plot([1,6],[1,6], linestyle="-.", linewidth=0.6, color="grey")

    plt.title("Part 2b: Scaling of Applications")
    plt.xlabel("number of threads")
    plt.ylabel("speedup")

    plt.xticks([x for x in range(0,13)])
    # plt.yticks([y for y in range(0, 11, 1)])
    plt.legend(title='application', loc='upper left')
    ax = plt.gca()
    ax.set_facecolor('#F4F3F5')

    plt.grid()
    plt.show()
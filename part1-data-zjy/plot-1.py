from audioop import avg
import numpy as np
import matplotlib.pyplot as plt

def read(filename):
    f = open(filename)
    x1, x2, x3 , l1, l2 ,l3 = [], [], [], [], [], []
    for i, lines in enumerate(f.readlines()):
        if i >= 1 and i <= 16:
            l1.append(float(lines.split()[-6])/1000)
            x1.append(float(lines.split()[-2]))
        elif i >= 20 and i<=35:
            l2.append(float(lines.split()[-6])/1000)
            x2.append(float(lines.split()[-2]))
        elif i >= 39 and i<=54:
            l3.append(float(lines.split()[-6])/1000)
            x3.append(float(lines.split()[-2]))
    x_avg = [sum(x)/3 for x in zip(x1,x2,x3)]   
    x_std = [np.std(x) for x in zip(x1,x2,x3)]   
    l_avg = [sum(x)/3 for x in zip(l1,l2,l3)]
    l_std = [np.std(x) for x in zip(l1,l2,l3)]
    return l_avg, l_std, x_avg, x_std

rawy_avg, rawy_std, rawx_avg, rawx_std = read("raw.txt")
cpuy_avg, cpuy_std, cpux_avg, cpux_std = read("cpu.txt")
l1dy_avg, l1dy_std, l1dx_avg, l1dx_std = read("l1d.txt")
l1iy_avg, l1iy_std, l1ix_avg, l1ix_std = read("l1i.txt")
l2y_avg, l2y_std, l2x_avg, l2x_std = read("l2.txt")
llcy_avg, llcy_std, llcx_avg, llcx_std = read("llc.txt")
memy_avg, memy_std, memx_avg, memx_std = read("membw.txt")

msize = 5
m = "o"
medge = 0.5
mfill='none'
mecolor = "w"
lwidth = 1.2
plotstyle=''

def plotline(x, y, xerr, yerr, labelname):
    plt.errorbar(x, y, xerr=xerr, yerr=yerr,fmt=plotstyle, linewidth=lwidth, markersize=msize,marker = m,markeredgewidth=medge,markeredgecolor=mecolor,capsize=3,capthick=1, label=labelname)



fig = plt.figure()
plotline(rawx_avg, rawy_avg, rawx_std, rawy_std, "raw")
plotline(cpux_avg, cpuy_avg, cpux_std, cpuy_std, "cpu")
plotline(l1dx_avg, l1dy_avg, l1dx_std, l1dy_std, "l1d")
plotline(l1ix_avg, l1iy_avg, l1ix_std, l1iy_std, "l1i")
plotline(l2x_avg, l2y_avg, l2x_std, l2y_std, "l2")
plotline(llcx_avg, llcy_avg, llcx_std, llcy_std, "llc")
plotline(memx_avg, memy_avg, memx_std, memy_std, "membw")
# plt.errorbar(rawx_avg, rawy_avg, xerr=rawx_std, yerr=rawy_std,fmt=plotstyle, linewidth=lwidth, markersize=msize,marker = m, markerfacecolor='none',markeredgewidth=medge, markeredgecolor=mecolor,capsize=3,capthick=1, label='raw')
# plt.errorbar(cpux_avg, cpuy_avg, xerr=cpux_std, yerr=rawy_std,fmt=plotstyle, linewidth=lwidth, markersize=msize,marker = m, markerfacecolor='none',markeredgewidth=medge, markeredgecolor=mecolor,capsize=3,capthick=1, label='cpu')
# plt.errorbar(l1dx_avg, l1dy_avg, xerr=l1dx_std, yerr=l1dy_std,fmt=plotstyle, linewidth=lwidth, markersize=msize,marker = m, markerfacecolor='none',markeredgewidth=medge, markeredgecolor=mecolor,capsize=3,capthick=1, label='l1d')
# plt.errorbar(l1ix_avg, l1iy_avg, xerr=l1ix_std, yerr=l1iy_std,fmt=plotstyle, linewidth=lwidth, markersize=msize,marker = m, markerfacecolor='none',markeredgewidth=medge, markeredgecolor=mecolor,capsize=3,capthick=1, label='l1i')
# plt.errorbar(l2x_avg, l2y_avg, xerr=l2x_std, yerr=l2y_std,fmt=plotstyle, linewidth=lwidth, markersize=msize,marker = m, markerfacecolor='none',markeredgewidth=medge, markeredgecolor=mecolor,capsize=3,capthick=1, label='l2')
# plt.errorbar(llcx_avg, llcy_avg, xerr=llcx_std, yerr=llcy_std,fmt=plotstyle, linewidth=lwidth, markersize=msize,marker = m, markerfacecolor='none',markeredgewidth=medge, markeredgecolor=mecolor,capsize=3,capthick=1, label='llc')
# plt.errorbar(memx_avg, memy_avg, xerr=memx_std, yerr=memy_std,fmt=plotstyle, linewidth=lwidth, markersize=msize,marker = m, markerfacecolor='none',markeredgewidth=medge, markeredgecolor=mecolor,capsize=3,capthick=1, label='membw')
plt.legend(loc='upper left')
ax = plt.gca()
ax.set_facecolor('#EDECEF')
plt.grid()
plt.show()
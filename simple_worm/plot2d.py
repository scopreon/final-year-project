import numpy as np
from typing import *


from simple_worm.worm import Worm
import matplotlib.pyplot as plt
import statistics
from matplotlib.animation import FFMpegWriter

import csv

from simple_worm.frame import FrameSequenceNumpy

# Live plots a clip
def plot_midline(FS, dt = 0.001, speed = 1, xlim = [-1,3], ylim = [-3,1]):
    xdata = []
    ydata = []
    i = 0
    skip = (1/(10 * dt))*speed #10fps
    for f in FS:
        # if i % skip == 0:
        plt.cla()
        plt.xlim(xlim[0], xlim[1])
        plt.ylim(ylim[0], ylim[1])
        plt.plot(f.x[0], f.x[2])
        
        # print(type(f.x[0]), f.x[0])
        # print(type(f.x[2]), f.x[2])
        plt.pause(0.1)
        # i += 1
    plt.show()

#Saves a csv of the midline data
def FS_to_midline_csv(FS, name = "midline"): #code based on examples from https://docs.python.org/3/library/csv.html
    with open(name + '.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        i = 0
        for f in FS:
            csvwriter.writerow(f.x[0])
            csvwriter.writerow(f.x[2])

#generates an mp4 from the midline data in a csv   
#based off CodingLikeMad's tutorial https://www.youtube.com/watch?v=bNbN9yoEOdU 
def clip_midline_csv(sourcename = "midline", outname = "midline", dt = 0.001, speed = 1, xlim = [-1,3], ylim = [-3,1]):
    skip = ((1/(25 * dt))*2)*speed #25 frames per second
    if skip % 2 == 1:
        skip -= 1
    with open(sourcename + '.csv', 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        data = np.float_(list(csvreader))
    # data = parse_csv_data(sourcename + '.csv')
    print(data)
    fig = plt.figure()
    plot, = plt.plot([],[],'k-')
    plt.xlim(xlim[0], xlim[1])
    plt.ylim(ylim[0], ylim[1])
    
    metadata = dict(title=outname, artist='simple-worm')
    writer = FFMpegWriter(fps=25, metadata=metadata)
    print(len(data))
    with writer.saving(fig, outname + ".mp4", 100):
        for i in range(0, len(data), 2):
            plot.set_data(data[i], data[i+1])
            writer.grab_frame()

#plots a kymograph from a csv containing alpha data    
def plot_kymograph_csv(name = "alpha", sample=10, highlight=""):
    with open(name + '.csv', 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        data = np.float_(list(csvreader))
    graph_data = np.zeros((int(len(data)/sample), len(data[0])))
    xdata = []
    ydata = []
    for i in range(1, len(graph_data)-1):
        graph_data[i] = data[i*sample]
        if highlight != "":
            for l in range(0, len(data[0])):
                if highlight == "zeros" and ((data[i*sample][l] > 0 and data[(i-1)*sample][l] < 0) or (data[i*sample][l] < 0 and data[(i-1)*sample][l] > 0)):
                    xdata.append(i)
                    ydata.append(l)
                elif highlight == "max" and data[i*sample][l] > data[(i-1)*sample][l] and data[i*sample][l] > data[(i+1)*sample][l]:
                    xdata.append(i)
                    ydata.append(l)
    ax = plt.figure(figsize=(6, 6))
    plt.imshow(np.transpose(graph_data), cmap='plasma', origin='lower')
    plt.scatter(xdata, ydata, c='r', marker=".")
    plt.show()

#obtains a frequency by measuring the timesteps between lines of zero-curvature    
def csv_to_frequency(name = "alpha", dt=0.001):
    with open(name + '.csv', 'r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        data = np.float_(list(csvreader))
    nseg = len(data[0])
    ts = []
    t = 0
    for l in range(1, 48):
        t=0
        for i in range(0, len(data)):
            t += dt
            if (data[i][12] > 0 and data[i-1][12] < 0):
                ts.append(t)
                t=0
    print(ts)
    return statistics.mean(ts)

def multiple_FS_to_clip(worms: [str, FrameSequenceNumpy], outname = "midline", dt = 0.001, speed = 1, xlim = [-1,3], ylim = [-3,1]):
    fig = plt.figure()

    colors = "bgrcmk"

    plots = [plt.plot([],[],'k-', color='#'+str(w % 10) * 6, label=f"{w}: {worms[w][0]}")[0] for w in range(len(worms))]
    labels = [plt.text(0,0,str(i),verticalalignment='bottom', horizontalalignment='left') for i in range(len(worms))]

    data=[[] for _ in range(len(worms))]
    print(data)
    for i, (name, FS) in enumerate(worms):
        for f in FS:
            data[i].append(np.float_(f.x[0]))
            data[i].append(np.float_(f.x[2]))

    data = np.float_(data)
    plt.plot(xlim,[0,0],linestyle='dotted',alpha=0.5)
    plt.xlim(xlim[0], xlim[1])
    plt.ylim(ylim[0], ylim[1])
    plt.legend()
    metadata = dict(title=outname, artist='simple-worm')
    writer = FFMpegWriter(fps=25, metadata=metadata)
    print(len(data))
    with writer.saving(fig, "2Dvids/"+outname + ".mp4", 100):
        for i in range(0, len(data[0]), 2):
            for j, (label,plot) in enumerate(zip(labels,plots)):
                plot.set_data(data[j][i], data[j][i+1])
                label.set_position((data[j][i][0], data[j][i+1][0]))
                

            writer.grab_frame()

def multiple_worm_path()
    break
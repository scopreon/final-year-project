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
from matplotlib.colors import LinearSegmentedColormap
def multiple_FS_to_clip(worms, outname="midline", dt=0.001, speed=1, xlim=[-1,3], ylim=[-3,1], concentration_func=None):
    fig, ax = plt.subplots()

    colors = "bgrcmk"

    plots = [ax.plot([], [], 'k-', color='#' + str(w % 10) * 6, label=f"{w}: {worms[w][0]}")[0] for w in range(len(worms))]
    labels = [ax.text(0, 0, str(i), verticalalignment='bottom', horizontalalignment='left') for i in range(len(worms))]

    data = [[] for _ in range(len(worms))]
    for i, (name, FS) in enumerate(worms):
        for f in FS:
            data[i].append(np.float_(f.x[0]))
            data[i].append(np.float_(f.x[2]))

    data = np.float_(data)
    ax.plot(xlim, [0, 0], linestyle='dotted', alpha=0.5)
    ax.set_xlim(xlim[0], xlim[1])
    ax.set_ylim(ylim[0], ylim[1])
    ax.legend()

    if concentration_func is not None:
        x = np.linspace(xlim[0], xlim[1], 100)
        y = np.linspace(ylim[0], ylim[1], 100)
        X, Y = np.meshgrid(x, y)
        Z = concentration_func(X, Y)
        Z = Z / Z.max()  # Normalize Z for better visualization
        single_color_cmap = LinearSegmentedColormap.from_list("custom_blue", ["#add8e6", "#00008b"])
        ax.imshow(Z, cmap=single_color_cmap, aspect='auto', extent=[xlim[0], xlim[1], ylim[0], ylim[1]], origin='lower')

    metadata = dict(title=outname, artist='simple-worm')
    writer = FFMpegWriter(fps=25, metadata=metadata)

    with writer.saving(fig, "2Dvids/" + outname + ".mp4", 100):
        for i in range(0, len(data[0]), 2):
            for j, (label, plot) in enumerate(zip(labels, plots)):
                plot.set_data(data[j][i], data[j][i + 1])
                label.set_position((data[j][i][0], data[j][i + 1][0]))
                

            writer.grab_frame()

# draws the path of the worms, changes window size dynamically
# def multiple_worm_path(worms: [str, FrameSequenceNumpy], outname = "midline", xlim = [-1,3], ylim = [-3,1]):
#     data=[[] for _ in range(len(worms))]
#     for i, (name, FS) in enumerate(worms):
#         for f in FS:
#             data[i].append((np.float_(f.x[0][0]),np.float_(f.x[2][0])))
    
#     plt.figure()
#     for line in data:
#     # Unpack the points into x and y coordinates
#         x, y = zip(*line)
#         plt.plot(x, y) 

#     plt.title('Line Shapes Plot')
#     plt.xlabel('X axis')
#     plt.ylabel('Y axis')

#     # Show the plot
#     # plt.show()

#     # Save the plot to a file
#     print(outname)
#     plt.savefig(outname)
#     plt.close()





def multiple_worm_path_matrix(worms: [(str, 'FrameSequenceNumpy')], outname="midline", xlim=[-1, 3], ylim=[-3, 1]):
    # Determine the size of the grid
    # positions = [name for name, _ in worms]
    # grid_x = max(x for x, _ in positions) + 1
    # grid_y = max(y for _, y in positions) + 1
    grid_x = int(np.ceil(np.sqrt(len(worms))))
    grid_y = grid_x
    
    # Create a figure with subplots in a matrix grid formation
    fig, axs = plt.subplots(grid_y, grid_x, figsize=(grid_x * 5, grid_y * 5))

    # Ensure axs is a 2D array for consistency in indexing
    if grid_x == 1 or grid_y == 1:
        axs = np.array(axs).reshape(grid_y, grid_x)
    
    # Initialize a blank list to store plot data for each worm
    data = [[] for _ in range(len(worms))]
    for i, (name, FS) in enumerate(worms):
        # Extract the subplot position from the worm's name
        # pos_x, pos_y = map(int, name.split('_'))
        pos_x, pos_y = int(i/grid_x), int(i%grid_y)
        for f in FS:
            data[i].append((np.float_(f.x[0][0]), np.float_(f.x[2][0])))
        
        # Plot each worm's path in its corresponding subplot
        x, y = zip(*data[i])
        axs[pos_y, pos_x].plot(x, y)
        axs[pos_y, pos_x].set_xlim(xlim)
        axs[pos_y, pos_x].set_ylim(ylim)
        axs[pos_y, pos_x].set_title(f'Worm at {name}')
    
    # Set a main title and adjust layout
    plt.suptitle('Multiple Worm Paths in Matrix Grid')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the plot to a file
    print(outname)
    plt.savefig(outname)
    plt.close()

# Note: 'FrameSequenceNumpy' should be replaced with the appropriate type for FS if needed.

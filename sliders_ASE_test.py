from simple_worm.steering_circuit import SteeringCircuit
from simple_worm.steering_parameters import SteeringParameters
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import configparser
import numpy as np

# Initial parameters
dt = 0.01
SYNAPSES = [0, 0, 0, 0, 0, 0, 0]
THRESHOLDS = [0, 0, 0, 0, 0]
JUNCTIONS = [1,1]

def load_parameters(filename='parameters.ini'):
    global SYNAPSES, THRESHOLDS
    
    config = configparser.ConfigParser()
    config.read(filename)
    
    if 'SYNAPSES' in config and 'THRESHOLDS' in config:
        SYNAPSES = [float(config['SYNAPSES'][f'synapse_{i}']) for i in range(len(config['SYNAPSES']))]
        THRESHOLDS = [float(config['THRESHOLDS'][f'threshold_{i}']) for i in range(len(config['THRESHOLDS']))]
        print("Parameters loaded from", filename)
        # Optionally, update any UI elements like sliders here based on the loaded values
    else:
        print("Error: Invalid configuration file or missing sections.")

# Example usage
# load_parameters('parameters.ini')

def save_parameters(event):
    config = configparser.ConfigParser()
    config['SYNAPSES'] = {f'synapse_{i}': str(val) for i, val in enumerate(SYNAPSES)}
    config['THRESHOLDS'] = {f'threshold_{i}': str(val) for i, val in enumerate(THRESHOLDS)}
    with open('parameters.ini', 'w') as configfile:
        config.write(configfile)
    print("Parameters saved to parameters.ini")


# Create the simulation function
def simulate(SYNAPSES, THRESHOLDS):
    params = SteeringParameters(SYNAPSES=SYNAPSES, THRESHOLDS=THRESHOLDS, JUNCTIONS=JUNCTIONS)
    circuit = SteeringCircuit(dt, params)
    points = []
    for x in range(1000):
        value = 1 if 300 < x < 500 else 0
        circuit.update_state(concentration=value)
        points.append((circuit.ASE[0].output(), circuit.ASE[1].output(), circuit.AIY[0].output(), circuit.AIY[1].output(), circuit.AIZ[0].output(), circuit.AIZ[1].output()))
    return points

lines = []

# Plotting function
def update(val):
    for i, slider in enumerate(syn_sliders):
        SYNAPSES[i] = slider.val
    for i, slider in enumerate(thr_sliders):
        THRESHOLDS[i] = slider.val
    points = simulate(SYNAPSES, THRESHOLDS)
    ase_series = list(zip(*points))
    for line, ase in zip(lines, ase_series):
        line.set_ydata(ase)  # Update the plot data
    fig.canvas.draw_idle()

# Setup the figure and axes for the sliders and the plot
fig, axs = plt.subplots(6,1,figsize=(10, 8))
plt.subplots_adjust(left=0.1, bottom=0.2, right=0.65)

# Create axes for sliders on the right
slider_position = 0.7  # Starting position for sliders
slider_height = 0.03
slider_width = 0.2
vertical_spacing = 0.04

# Initial simulation to get the starting data
points = simulate(SYNAPSES, THRESHOLDS)
ase_series = list(zip(*points))
time_series = [x * dt for x in range(1000)]

# Plot data
for i, (ax, ase) in enumerate(zip(axs, ase_series)):
    line, = ax.plot(time_series, ase, label=f'ASE {i}')
    lines.append(line)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('ASE Value')
    ax.set_ylim(0,1)
    ax.set_title(f'ASE {i} Over Time')
    ax.legend()

# Add sliders for SYNAPSES and THRESHOLDS
syn_sliders = []
thr_sliders = []
for i in range(len(SYNAPSES)):
    axsyn = plt.axes([slider_position, 1 - (slider_height + vertical_spacing) * (i + 1), slider_width, slider_height], facecolor='lightgoldenrodyellow')
    syn_sliders.append(Slider(axsyn, f'Syn {i}', -15.0, 15.0, valinit=SYNAPSES[i]))

for i in range(len(THRESHOLDS)):
    axthr = plt.axes([slider_position, 1 - (slider_height + vertical_spacing) * (len(SYNAPSES) + i + 1), slider_width, slider_height], facecolor='lightsteelblue')
    thr_sliders.append(Slider(axthr, f'Thr {i}', -15.0, 15.0, valinit=THRESHOLDS[i]))

plt.subplots_adjust(bottom=0.2)  # Adjust layout to make room for the button
button_ax = plt.axes([0.8, 0.05, 0.1, 0.075])  # Adjust as necessary for your layout
button = Button(button_ax, 'Save', color='lightgoldenrodyellow', hovercolor='0.975')
button.on_clicked(save_parameters)


# Set the update function for the sliders
for slider in syn_sliders + thr_sliders:
    slider.on_changed(update)

plt.show()

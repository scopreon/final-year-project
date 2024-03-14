from simple_worm.steering_circuit import SteeringCircuit
from simple_worm.steering_parameters import SteeringParameters
import matplotlib.pyplot as plt
import numpy as np

dt = 0.01
SYNAPSES = [0,0,0,0,0,0,0]
THRESHOLDS = [0,0,0,0,0]

params = SteeringParameters(SYNAPSES=SYNAPSES, THRESHOLDS=THRESHOLDS)
circuit = SteeringCircuit(params, dt)
points = []
for x in range(0,1000):
    value = 1 if 300 < x < 500 else 0
    circuit.update_state(concentration=value)
    points.append((circuit.ASE[0], circuit.ASE[1], circuit.AIY[0], circuit.AIY[1], circuit.AIZ[0], circuit.AIZ[1]))

ase_series = list(zip(*points))
time_series = [x * 0.01 for x in range(1000)]
num_ase_series = len(ase_series)
plt.figure(figsize=(10, 2 * num_ase_series))  # Adjust the figure height dynamically based on the number of plots

for i, ase in enumerate(ase_series):
    plt.subplot(num_ase_series, 1, i + 1)  # Dynamically position each plot
    plt.plot(time_series, ase, label=f'ASE {i}')
    plt.xlabel('Time (s)')
    plt.ylabel('ASE Value')
    plt.title(f'ASE {i} Over Time')
    plt.legend()

plt.tight_layout()  # Adjust the layout to make sure there's no overlap
plt.show()
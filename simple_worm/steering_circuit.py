import numpy as np
from collections import deque
from simple_worm.steering_parameters import SteeringParameters
import math
import configparser

def sigmoid(x):
  return 1 / (1 + math.exp(-x))


class Neurone:
    def __init__(self, threshold, time_const) -> None:
        self.potential = 0
        self.threshold = threshold
        self.time_const = time_const

class SensorNeuron(Neurone):
    def __init__(self, threshold, time_const) -> None:
        super().__init__(threshold, time_const)
    def output(self):
        return self.potential

class InterNeuron(Neurone):
    def __init__(self, threshold, time_const) -> None:
        super().__init__(threshold, time_const)
    def output(self):
        return sigmoid(self.potential + self.threshold)


class SteeringCircuit:
    def __init__(self, dt, parameters: SteeringParameters = SteeringParameters(), parameters_filename: str = None) -> None:
        if parameters_filename is None:
            self.parameters = parameters
        else:
            config = configparser.ConfigParser()
            config.read(parameters_filename)
            
            if 'SYNAPSES' in config and 'THRESHOLDS' in config:
                SYNAPSES = [float(config['SYNAPSES'][f'synapse_{i}']) for i in range(len(config['SYNAPSES']))]
                THRESHOLDS = [float(config['THRESHOLDS'][f'threshold_{i}']) for i in range(len(config['THRESHOLDS']))]
                self.parameters = SteeringParameters(SYNAPSES=SYNAPSES, THRESHOLDS=THRESHOLDS)
                print("Parameters loaded from", parameters_filename)
                # Optionally, update any UI elements like sliders here based on the loaded values
            else:
                print("Error: Invalid configuration file or missing sections.")

        history_size = int((self.parameters.M + self.parameters.N)/dt)
        self.concentrations = deque(maxlen=history_size)

        # assert Decimal(str(self.steering_parameters.M)) % Decimal(str(dt)) == 0
        # assert Decimal(str(self.steering_parameters.N)) % Decimal(str(dt)) == 0

        self.dt = dt

        self.ASE = [SensorNeuron(parameters.thresholds[0], parameters.time_consts[0]), SensorNeuron(parameters.thresholds[0], parameters.time_consts[0])]
        self.AIY = [InterNeuron(parameters.thresholds[1], parameters.time_consts[1]), InterNeuron(parameters.thresholds[1], parameters.time_consts[1])]
        self.AIZ = [InterNeuron(parameters.thresholds[2], parameters.time_consts[2]), InterNeuron(parameters.thresholds[2], parameters.time_consts[2])]

        # weights coming out of neuron
        self.ASE_w = parameters.synapses[0:2]
        self.AIY_w = parameters.synapses[3]
        self.AIZ_w = parameters.synapses[4]

        self.AIY_gap = parameters.junctions[0]
        self.AIZ_gap = parameters.junctions[1]
            

    def get_differential(self, concentration):
        self.concentrations.append(concentration)
        len_concentrations = len(self.concentrations)

        start_M = max(0, len_concentrations - int(self.parameters.N/self.dt) - int(self.parameters.M/self.dt))
        end_M = max(0, len_concentrations - int(self.parameters.N/self.dt))
        cM = np.mean(list(self.concentrations)[start_M:end_M]) if start_M != end_M else 0

        start_N = max(0, len_concentrations - int(self.parameters.N/self.dt))
        cN = np.mean(list(self.concentrations)[start_N:]) if start_N < len_concentrations else 0

        # Update sensors based on the differential calculation
        differential = cN - cM

        return differential

        


    def update_state(self,concentration):
        differential = self.get_differential(concentration)

        self.ASE[0].potential += (max(0,differential) - self.ASE[0].potential) * self.dt / self.ASE[0].time_const
        self.ASE[1].potential += (max(0,-differential) - self.ASE[1].potential) * self.dt / self.ASE[0].time_const

        self.AIY[0].potential += (((self.ASE_w[0] * self.ASE[0].output() + self.ASE_w[1] * self.ASE[1].output()) - self.AIY[0].potential) + (self.AIY_gap * (self.AIY[1].potential - self.AIY[0].potential))) * self.dt / self.AIY[0].time_const
        self.AIY[1].potential += (((self.ASE_w[1] * self.ASE[0].output() + self.ASE_w[0] * self.ASE[1].output()) - self.AIY[1].potential) + (self.AIY_gap * (self.AIY[0].potential - self.AIY[1].potential))) * self.dt / self.AIY[0].time_const

        self.AIZ[0].potential = (((self.AIY_w * sigmoid(self.AIY[0].potential + self.AIY[0].threshold)) - self.AIZ[0].potential) + (self.AIZ_gap * (self.AIZ[1].potential - self.AIZ[0].potential))) * self.dt / self.AIZ[0].time_const
        self.AIZ[1].potential = (((self.AIY_w * sigmoid(self.AIY[1].potential + self.AIY[1].threshold)) - self.AIZ[1].potential) + (self.AIZ_gap * (self.AIZ[0].potential - self.AIZ[1].potential))) * self.dt / self.AIZ[1].time_const

    
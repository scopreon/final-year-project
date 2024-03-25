from simple_worm.worm_environment import Environment
from simple_worm.worm import Worm
from simple_worm.plot2d import *
from simple_worm.plot3d import *
from simple_worm.material_parameters import *
from simple_worm.neural_circuit import *
from simple_worm.neural_parameters import NeuralParameters
from simple_worm.steering_parameters import SteeringParameters
import itertools
import numpy
import os
from datetime import datetime

import numpy as np

def create_gradient_func(gradient_type, a, b, ya, yb, x1):
    """
    Creates a lambda function for either a linear or Gaussian gradient between values a and b,
    within the range y = ya to y = yb, starting at x = x1. Outside of this range, the function returns 0.
    
    :param gradient_type: 'linear' or 'gaussian'
    :param a: Starting value of the gradient
    :param b: Ending value of the gradient
    :param ya: Starting y value
    :param yb: Ending y value
    :param x1: Starting x value
    :return: Lambda function implementing the specified gradient
    """
    if gradient_type == "linear":
        # Linear gradient function
        # return lambda x, y: ((b-a)/(yb-ya)) * (y-ya) + a if ya <= y <= yb and x >= x1 else 0
        return lambda x, y: np.where((ya <= y) & (y <= yb) & (x >= x1), ((b-a)/(yb-ya)) * (y-ya) + a, 0)
    elif gradient_type == "gaussian":
        # Gaussian gradient function, adjusting parameters to fit the input criteria
        c = (yb-ya)/2  # Adjust the width based on the y-range
        y_mid = (ya+yb)/2
        return lambda x, y: (b-a) * np.exp(-((y-y_mid)**2)/(2*c**2)) + a if ya <= y <= yb else 0
    else:
        raise ValueError("Invalid gradient type. Choose 'linear' or 'gaussian'.")

os.remove("neuron_data.csv") 
folder = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

nested_directory_path = './runs/' + folder
os.makedirs(nested_directory_path, exist_ok=True)

# Example usage
# env = Environment()
# env.add_parameter('concentration', lambda x, y: (5-y * 0.1))
# seq = []
# myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[0,0], AVB=0.405), environment=env)
# seq.append(["Wormle", myworm.solve(5, MP=MaterialParametersFenics(), reset=True).to_numpy()])
# multiple_FS_to_clip(seq, outname="wormle", xlim=[-1,5], concentration_func=env.get_parameter_func('concentration'))
env = Environment()
env.add_parameter('concentration',create_gradient_func('linear',0,300,-2,2,-1))
# env.add_parameter('concentration',lambda x,y:)

print(env.get_parameters_at(5,-1)['concentration'])
print(env.get_parameters_at(5,0.5)['concentration'])

# exit(0)
seq = []
steering_params = SteeringParameters(filename='parameters.ini')

myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[0,0], STEERING_PARAMETERS=steering_params, STEERING=True, AVB = 0.405), quiet = True, environment=env)
seq.append([f'Worm1', myworm.solve(10, MP=MaterialParametersFenics(), reset=True).to_numpy()])


env = Environment()
env.add_parameter('concentration',create_gradient_func('linear',300,0,-2,2,-1))



myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[0,0], STEERING_PARAMETERS=steering_params, STEERING=True, AVB = 0.405), quiet = True, environment=env)
seq.append([f'Worm2', myworm.solve(10, MP=MaterialParametersFenics(), reset=True).to_numpy()])



data = [[] for _ in range(len(seq))]
for i, (name, FS) in enumerate(seq):
    for f in FS:
        data[i].append(np.float_(f.x[0]))
        data[i].append(np.float_(f.x[2]))

filename = f"{nested_directory_path}/my_data.csv"  # Path where the CSV file will be saved
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    for i in range(0, len(data[0]), 2):
        for j in len(data)
            (data[j][i][0], data[j][i + 1][0])
        writer.writerow()


multiple_worm_path(seq, outname=f"{nested_directory_path}/path", xlim=[-1,10], ylim=[-5,5])
multiple_FS_to_clip(seq, outname=f"{nested_directory_path}/vid", xlim=[-1,10], ylim=[-5,5], concentration_func=env.get_parameter_func('concentration'))
steering_params.save_parameters(f"{nested_directory_path}/params")
# plot_neurones()
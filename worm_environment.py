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


# Example usage
# env = Environment()
# env.add_parameter('concentration', lambda x, y: (5-y * 0.1))
# seq = []
# myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[0,0], AVB=0.405), environment=env)
# seq.append(["Wormle", myworm.solve(5, MP=MaterialParametersFenics(), reset=True).to_numpy()])
# multiple_FS_to_clip(seq, outname="wormle", xlim=[-1,5], concentration_func=env.get_parameter_func('concentration'))
env = Environment()
# env.add_parameter('concentration', lambda x, y: np.where(y > 1, 1, np.where(y < -1, 0, (1 - (y + 1) / 2))))

# env.add_parameter('concentration', lambda x, y: np.where(y > 1, 30, np.where(y < -1, 0, 30 * (1 - (y + 1) / 2))))
env.add_parameter('concentration', lambda x, y: np.where(x <= 3, 0, np.where(y > 1, 0, np.where(y < -1, 0, 10 * (1 - (y + 1) / 2)))))

seq = []
steering_params = SteeringParameters(filename='parameters.ini')


# for x in [0.441,0.442,0.443,0.444,0.445,0.446,0.447,0.448]:
    # print(x)
# myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[0,0], STEERING_PARAMETERS=steering_params, STEERING=True, AVB = 0.405), quiet = True, environment=env)
# seq.append([f'Wormle1', myworm.solve(10, MP=MaterialParametersFenics(), reset=True).to_numpy()])

# steering_params.synapses[4],steering_params.synapses[5] = steering_params.synapses[5],steering_params.synapses[4]
# print(steering_params.synapses)

# myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[0,0], STEERING_PARAMETERS=steering_params, STEERING=False, AVB = 0.405), quiet = True, environment=env)
# seq.append([f'Wormle2', myworm.solve(10, MP=MaterialParametersFenics(), reset=True).to_numpy()])

myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[0,0], STEERING_PARAMETERS=steering_params, STEERING=True, AVB = 0.405), quiet = True, environment=env)
seq.append([f'Wormle5', myworm.solve(10, MP=MaterialParametersFenics(), reset=True).to_numpy()])


# steering_params.synapses[4],steering_params.synapses[5] = steering_params.synapses[5],steering_params.synapses[4]

# env2 = Environment()
# env2.add_parameter('concentration', lambda x, y: np.where(y > 1, 1, np.where(y < -1, 0, (1 - (-y + 1) / 2))))

# myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[0,0], STEERING_PARAMETERS=steering_params, STEERING=True, AVB = 0.405), quiet = True, environment=env2)
# seq.append([f'Wormle3', myworm.solve(10, MP=MaterialParametersFenics(), reset=True).to_numpy()])

# myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[0,0], AVB=0.405,STEERING_PARAMETERS=steering_params, STEERING=False), environment=env)
# seq.append(["Wormle", myworm.solve(5, MP=MaterialParametersFenics(), reset=True).to_numpy()])

# multiple_FS_to_clip(seq, outname="wormle7", xlim=[-1,10], ylim=[-5,5] , concentration_func=env.get_parameter_func('concentration'))
multiple_worm_path(seq, outname="test/wormle1", xlim=[-1,10], ylim=[-5,5])
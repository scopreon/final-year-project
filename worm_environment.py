from simple_worm.worm_environment import Environment
from simple_worm.worm import Worm
from simple_worm.plot2d import *
from simple_worm.plot3d import *
from simple_worm.material_parameters import *
from simple_worm.neural_circuit import *
from simple_worm.neural_parameters import NeuralParameters
import itertools
import numpy

# Example usage
env = Environment()
# env.add_parameter('concentration', lambda x, y: x * 0.1)
env.add_parameter('concentration', lambda x, y: np.sqrt(x**2 + y**2))


seq = []
myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[0,0]), environment=env)
seq.append(["Wormle", myworm.solve(1, MP=MaterialParametersFenics(), reset=True).to_numpy()])
multiple_FS_to_clip(seq, outname="wormle", xlim=[-1,5], concentration_func=env.get_parameter_func('concentration'))

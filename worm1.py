from simple_worm.worm import Worm
from simple_worm.plot2d import *
from simple_worm.plot3d import *
from simple_worm.material_parameters import *
from simple_worm.neural_circuit import *
from simple_worm.neural_parameters import NeuralParameters
import time

# MP = MaterialParametersFenics(K=10)

t0 = time.time()



K_VALUES = [x for x in range(10,101,10)]
seq = []
for K in K_VALUES:
    myworm = Worm(N=48, dt=0.01, neural_control=True)
    seq.append([K,myworm.solve(3, MP=MaterialParametersFenics(K=K), reset=True).to_numpy()])

t1 = time.time()
print(f"TOTAL RUN TIME: {t1-t0}")



multiple_FS_to_clip(seq)





# ,seq4.to_numpy()

# # plot_midline(seq)
# FS_to_midline_csv(seq)
#     # print(len(FS))
# clip_midline_csv()


# plot_midline(seq)

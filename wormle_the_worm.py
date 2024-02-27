from simple_worm.worm import Worm
from simple_worm.plot2d import *
from simple_worm.plot3d import *
from simple_worm.material_parameters import *
from simple_worm.neural_circuit import *
from simple_worm.neural_parameters import NeuralParameters
import itertools

# print()
# NP=NeuralParameters(AVB=0.405, SYMMETRIC_AVB=False)
# NP=NeuralParameters(AVB=0.405, AVB_D=1.0,AVB_V=0.0, SYMMETRIC_AVB=False)


# myworm = Worm(N=48, dt=0.1, neural_control=True)
# seq=[]
# seq.append(["Wormle",myworm.solve(3, MP=MaterialParametersFenics(), reset=True).to_numpy()])
# multiple_FS_to_clip(seq, outname="0.1")

# myworm = Worm(N=48, dt=0.001, neural_control=True)
# seq=[]
# seq.append(["Wormle",myworm.solve(3, MP=MaterialParametersFenics(), reset=True).to_numpy()])
# multiple_FS_to_clip(seq, outname="0.001")
final_y_coords = []
seq=[]
# for i,j in itertools.permutations([x for x in [-0.6,0.4,-0.2,0,0.2,0.4,0.6]], r=2):
for (i,j) in [(-0.5,0.5),(0.5,-0.5)]:
    print(i,j)
    myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[i,j], AVB=0.405))
    seq.append([i, myworm.solve(10, MP=MaterialParametersFenics(), reset=True).to_numpy()])
    final_y_coords.append([i,j,myworm.get_x()[2][0]])
    # break
    

for x in final_y_coords:
    print(x)
multiple_FS_to_clip(seq, outname="left_turn", xlim=[-1,5])

# myworm = Worm(N=48, dt=0.001, neural_control=True)
# seq=[]
# seq.append(["Wormle",myworm.solve(3, MP=MaterialParametersFenics(), reset=True).to_numpy()])
# multiple_FS_to_clip(seq, outname="0.001")




# ,seq4.to_numpy()

# # plot_midline(seq)
# FS_to_midline_csv(seq)
#     # print(len(FS))
# clip_midline_csv()


# plot_midline(seq)

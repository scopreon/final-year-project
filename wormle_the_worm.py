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
perms = itertools.permutations([x for x in [-0.6,-0.4,-0.2,0,0.2,0.4,0.6]], r=2)
perms = itertools.product([-0.6,-0.4,-0.2,0],[0.6,0.4,0.2,0])
# print(*perms)

for i,j in perms:
# for (i,j) in [(-x/10,x/10) for x in range(5,10,1)]:
    print(i,j)
    myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[i,j]))
    seq.append([(i,j), myworm.solve(10, MP=MaterialParametersFenics(), reset=True).to_numpy()])
    # final_y_coords.append([i,j,myworm.get_x()[2][0]])


    # break
    
# multiple_worm_path([seq[len(seq)-1]], outname=f"./pics/{int(i*10)}_{int(j*10)}", xlim=[-1,5])
# for x in final_y_coords:
#     print(x)
# multiple_FS_to_clip(seq, outname="left_turn", xlim=[-1,5])
multiple_worm_path_matrix(seq, outname=f"pics/{int(i*10)}_{int(j*10)}.png", xlim=[-1,5])

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

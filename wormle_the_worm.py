from simple_worm.worm import Worm
from simple_worm.plot2d import *
from simple_worm.plot3d import *
from simple_worm.material_parameters import *
from simple_worm.neural_circuit import *
from simple_worm.neural_parameters import NeuralParameters

# print()
# NP=NeuralParameters(AVB=0.405, SYMMETRIC_AVB=False)
# NP=NeuralParameters(AVB=0.405, AVB_D=1.0,AVB_V=0.0, SYMMETRIC_AVB=False)


myworm = Worm(N=48, dt=0.1, neural_control=True)
seq=[]
seq.append(["Wormle",myworm.solve(3, MP=MaterialParametersFenics(), reset=True).to_numpy()])
multiple_FS_to_clip(seq, outname="0.1")

myworm = Worm(N=48, dt=0.001, neural_control=True)
seq=[]
seq.append(["Wormle",myworm.solve(3, MP=MaterialParametersFenics(), reset=True).to_numpy()])
multiple_FS_to_clip(seq, outname="0.001")

myworm = Worm(N=48, dt=0.01, neural_control=True)
seq=[]
seq.append(["Wormle",myworm.solve(3, MP=MaterialParametersFenics(), reset=True).to_numpy()])
multiple_FS_to_clip(seq, outname="0.01")

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

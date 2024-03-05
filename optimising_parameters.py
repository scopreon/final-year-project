from simple_worm.worm import Worm
from simple_worm.plot2d import *
from simple_worm.plot3d import *
from simple_worm.material_parameters import *
from simple_worm.neural_circuit import *
from simple_worm.neural_parameters import NeuralParameters
import itertools
from concurrent.futures import ProcessPoolExecutor


def solve_worm(params):
    i, j = params
    myworm = Worm(
        N=48,
        dt=0.01,
        neural_control=True,
        NP=NeuralParameters(TEMP_VAR=[0, 0], AVB_D=i, AVB_V=j, SYMMETRIC_AVB=False),
    )
    result = myworm.solve(10, MP=MaterialParametersFenics(), reset=True).to_numpy()
    return (i, j), result


# with custom AVB


def main():
    perms = itertools.product(
        [x / 10 for x in range(0, 8, 2)], [x / 10 for x in range(-6, 1, 2)]
    )
    
    # print(len(list(perms)))
    perms = itertools.product(
        [x / 100 for x in range(0, 55, 10)],
        [x / 100 for x in range(50, 105, 10)],
    )
    results = []
    perms=[(0.405,0.405)]
    perms=[(x / 100,x/100) for x in range(0, 100, 5)]
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(solve_worm, perms))

    multiple_worm_path_matrix(
        results, outname=f"ABV_DEF.png", xlim=[-2, 10], ylim=[-10, 10]
    )


# def main():
#     final_y_coords = []
#     seq=[]
#     perms = itertools.product([x/10 for x in range(-6,7,1)], [x/10 for x in range(-6,7,1)])

#     for i,j in perms:
#         print(i,j)
#         myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[i,j], AVB=405))
#         seq.append([(i,j), myworm.solve(10, MP=MaterialParametersFenics(), reset=True).to_numpy()])


#     multiple_worm_path_matrix(seq, outname=f"ABV_405.png", xlim=[-1,5], ylim=[-3,3])

if __name__ == "__main__":
    main()

# for i,j in perms:
#     print(i,j)
#     myworm = Worm(N=48, dt=0.01, neural_control=True, NP = NeuralParameters(TEMP_VAR=[i,j]))
#     seq.append([(i,j), myworm.solve(10, MP=MaterialParametersFenics(), reset=True).to_numpy()])


# multiple_worm_path_matrix(seq, outname=f"ABV_DEF.png", xlim=[-1,5], ylim=[-3,3])


# with preset AVB

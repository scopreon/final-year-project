from concurrent.futures import ProcessPoolExecutor

from simple_worm.worm import Worm
from simple_worm.plot2d import *
from simple_worm.plot3d import *
from simple_worm.material_parameters import *
from simple_worm.neural_circuit import *

def solve_worm(K):
    myworm = Worm(N=48, dt=0.01, neural_control=True)
    result = [K,myworm.solve(3, MP=MaterialParametersFenics(K=K), reset=True).to_numpy()]
    return result

# MP = MaterialParametersFenics(K=10)
def main():
    K_VALUES = [x for x in range(10,101,10)]


    t0 = time.time()


    with ProcessPoolExecutor() as executor:
        results = list(executor.map(solve_worm,K_VALUES))
    
    
    t1 = time.time()
    print(f"TOTAL RUN TIME: {t1-t0}")


    multiple_FS_to_clip(results)
# ,seq4.to_numpy()

# # plot_midline(seq)
# FS_to_midline_csv(seq)
#     # print(len(FS))
# clip_midline_csv()


# plot_midline(seq)
if __name__ == "__main__":
    main()
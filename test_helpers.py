from simple_worm.test_helpers import *
from simple_worm.neural_parameters import NeuralParameters
from simple_worm.material_parameters import MaterialParameters
import time


def main():
    worm_num = 5
    # [(a,b,c),(a,b,c)]
    parameters = [[NeuralParameters(), MaterialParameters()] for x in range(worm_num)]

    # for K,(NP, MP) in zip([10,20,30,40],parameters):
    #     MP.K = K
    # for AVB, (NP, MP) in zip([0.2, 0.4, 0.6, 0.8], parameters):
    #     # MP.K = K
    #     NP.avb = AVB
    # for AVB, (NP, MP) in zip([0.2,0.3,0.4,0.45,0.5,0.6,0.7,0.8], parameters):
    #     # MP.K = K
    #     NP.avb = AVB
    # for AVB, (NP, MP) in zip([0.34,0.36,0.38,0.4,0.42,0.44,0.46], parameters):
    #     # MP.K = K
    #     NP.avb = AVB

    for AVB, (NP, MP) in zip([0.395,0.395,0.40,0.405,0.41], parameters):
        # MP.K = K
        NP.avb = AVB
    # for K, (NP,MP) in zip([10,101,10], parameters):
    #     NP.avb = 0.4
    #     NP.MP
        

    pool = WormPool(N=48, dt=0.01, worms_num=worm_num, parameters=parameters)

    t0 = time.time()
    pool.run(6)
    t1 = time.time()

    pool.create_clip(filename="SERIAL")

    print("TIMINGS")
    print(f"Serial:\t{t1-t0}")


# pool.create_clip()

if __name__ == "__main__":
    main()

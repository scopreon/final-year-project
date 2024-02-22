# This contains functions which can be used for easy parameter
# testing of the worm with different parameters

from enum import Enum, auto


from concurrent.futures import ProcessPoolExecutor, wait
from simple_worm.material_parameters import MaterialParameters
from simple_worm.neural_parameters import NeuralParameters
from simple_worm.worm import Worm
from simple_worm.plot2d import *


class WormStates(Enum):
    START: int = auto()
    RUNNING: int = auto()
    END: int = auto()


def run_worm(arg):
    # arg[0].run(arg[1])
    print("test")


def test(i):
    print("LOL")


class PoolWorm:
    w_id = 0
    NP = None
    MP = None
    worm = None
    FS = None  # frame sequence stored in numpy

    def __init__(
        self,
        w_id: int,
        N: int,
        dt: float,
        NP: NeuralParameters,
        MP: MaterialParameters,
    ):
        self.w_id = w_id
        self.NP = NP
        self.MP = MP
        print(MP.K)
        self.worm = Worm(N=N, dt=dt, NP=NP, neural_control=True)

    def run(
        self,
        time: float,
    ):
        try:
            print(f"Running for worm {self.w_id}")
            self.FS = self.worm.solve(time, reset=True, MP=self.MP).to_numpy()
            return 0
        except Exception as e:
            print("ERRORS")


class WormPool:
    worms = []
    state = WormStates.START

    def __init__(
        self,
        N: int,
        dt: float,
        worms_num: int,
        parameters: [(NeuralParameters, MaterialParameters)],
    ):
        assert worms_num == len(parameters)
        for i, (NP, MP) in enumerate(parameters):
            self.worms.append(PoolWorm(w_id=i, N=N, dt=dt, NP=NP, MP=MP))
            # self.worms[i].run(3)

    def run(
        self,
        time: float,
    ):
        for worm in self.worms:
            worm.run(time)
            pass

    def create_clip(self, filename: str = None):
        data = []
        for i, worm in enumerate(self.worms):
            data.append([i, worm.FS])
        multiple_FS_to_clip(data, outname=filename, ylim=[-2, 2], xlim=[0, 5])



# Generates a filename for a given worm experiment
def generate_file_name(
    worm_number: int,
    variable_changed: str,
    sim_time: int,
    dt: float,
    seg_num: int,
    range_1,
    turn,
    range_2=None,

):    
    # If there is no data range for i.e. only 1 value then don't include in filename
    data_range = f"{range_1}" + f"_{range_2}" if range_2 is not None else ""
    filename = f"{turn}_{variable_changed}_{data_range}_{sim_time}_{dt}_{worm_number}_{seg_num}"
    return filename

import numpy as np

SP_DEFAULT_M = 2
SP_DEFAULT_N = 2

SP_DEFAULT_SYNAPSES = np.array([1,-2,1,1,1,1,1])
SP_DEFAULT_JUNCTIONS = np.array([0,0])

SP_DEFAULT_TIME_CONSTANTS = np.array([0.1,0.1,0.1,0.1,0.1])

SP_DEFAULT_THRESHOLDS = np.array([-5,-5,-5,-5,-5])

class SteeringParameters:
    def __init__(
        self,
        M=SP_DEFAULT_M,
        N=SP_DEFAULT_N,
        SYNAPSES = SP_DEFAULT_SYNAPSES,
        JUNCTIONS = SP_DEFAULT_JUNCTIONS,
        TIME_CONSTANTS = SP_DEFAULT_TIME_CONSTANTS,
        THRESHOLDS=SP_DEFAULT_THRESHOLDS,
        TEMP_VAR=None
    ) -> None:
        self.M=M
        self.N=N
        self.synapses=SYNAPSES
        self.junctions=JUNCTIONS
        self.time_consts=TIME_CONSTANTS
        self.thresholds=THRESHOLDS
        self.temp_var = TEMP_VAR

import numpy as np

SP_DEFAULT_M = 0.5
SP_DEFAULT_N = 0.1

SP_DEFAULT_SYNAPSES = 0
SP_DEFAULT_JUNCTIONS = 0

SP_DEFAULT_TIME_CONSTANT = 0

class SteeringParameters:
    def __init__(
        self,
        M=SP_DEFAULT_M,
        N=SP_DEFAULT_N,
        SYNAPSES = SP_DEFAULT_SYNAPSES,
        JUNCTIONS = SP_DEFAULT_JUNCTIONS,
        TIME_CONSTANT = SP_DEFAULT_TIME_CONSTANT,
        TEMP_VAR=None
    ) -> None:
        self.M=M
        self.N=N
        self.synapses=SYNAPSES
        self.junctions=JUNCTIONS
        self.time_const=TIME_CONSTANT
        self.temp_var = TEMP_VAR

import numpy as np
import configparser

SP_DEFAULT_M = 0.1
SP_DEFAULT_N = 0.1


SP_DEFAULT_SYNAPSES = np.array([1,-1,1,1,1,1,1])
SP_DEFAULT_JUNCTIONS = np.array([0,0])

SP_DEFAULT_TIME_CONSTANTS = np.array([0.05,0.1,0.1,0.1,0.1])

SP_DEFAULT_THRESHOLDS = np.array([-5,-5,-5,-5,-5])






class SteeringParameters:
    def load_parameters(self, filename='parameters.ini'):
        config = configparser.ConfigParser()
        config.read(filename)
        
        if 'SYNAPSES' in config and 'THRESHOLDS' in config and 'JUNCTIONS' in config:
            self.synapses = [float(config['SYNAPSES'][f'synapse_{i}']) for i in range(len(config['SYNAPSES']))]
            self.thresholds = [float(config['THRESHOLDS'][f'threshold_{i}']) for i in range(len(config['THRESHOLDS']))]
            self.junctions = [float(config['JUNCTIONS'][f'junction_{i}']) for i in range(len(config['JUNCTIONS']))]
            print("Parameters loaded from", filename)
            # Optionally, update any UI elements like sliders here based on the loaded values
        else:
            print("Error: Invalid configuration file or missing sections.")
        
    def save_parameters(self, filename='parameters'):
        config = configparser.ConfigParser()
        config['SYNAPSES'] = {f'synapse_{i}': str(val) for i, val in enumerate(self.synapses)}
        config['THRESHOLDS'] = {f'threshold_{i}': str(val) for i, val in enumerate(self.thresholds)}
        config['JUNCTIONS'] = {f'junction_{i}': str(val) for i, val in enumerate(self.junctions)}
        with open(f'{filename}.ini', 'w') as configfile:
            config.write(configfile)
        print("Parameters saved to parameters.ini")

    def __init__(
        self,
        M=SP_DEFAULT_M,
        N=SP_DEFAULT_N,
        SYNAPSES = SP_DEFAULT_SYNAPSES,
        JUNCTIONS = SP_DEFAULT_JUNCTIONS,
        TIME_CONSTANTS = SP_DEFAULT_TIME_CONSTANTS,
        THRESHOLDS=SP_DEFAULT_THRESHOLDS,
        filename=None,
        TEMP_VAR=None
    ) -> None:
        if filename is not None:
            self.load_parameters(filename)
        else:
            self.thresholds=THRESHOLDS
            self.synapses=SYNAPSES
            self.junctions=JUNCTIONS
        self.M=M
        self.N=N
        self.time_consts=TIME_CONSTANTS
        self.temp_var = TEMP_VAR

import numpy as np
from simple_worm.neural_parameters import NeuralParameters
"""
Code in this file is based off of the model and software presented in:
J.H. Boyle, S. Berri and N. Cohen (2012), Gait modulation in C. elegans:
an integrated neuromechanical model, Front. Comput. Neurosci, 6:10 
doi: 10.3389/fncom.2012.00010

Under the licence below:

This software is freely available for use in research, teaching and other
non-commercial purposes.  Users have the right to modify, alter, improve,
or enhance the software without limitation, under the condition that you
do not remove or alter the copyright information in this section.

The original code is available at https://www.frontiersin.org/articles/10.3389/fncom.2012.00010
The structure and some comments from the original code are preserved for readability
"""

class NeuralModel:
    def __init__(self, N, dt, NP = NeuralParameters()):

        self.nseg = N  # Number of Segments in the body
        self.i_sr = np.zeros((self.nseg, 2))  # Input from stretch receptors
        self.l_sr = np.zeros((self.nseg, 2))  # Length of stretch receptors
        self.v_neuron = np.zeros((self.nseg, 2))  # Neuron state
        self.v_muscle = np.zeros((self.nseg, 2))  # Muscle state

        self.alpha0 = NP.alpha0 #curvature amplitude

        self.dt = dt

        # Neural parameters
        self.n_units = NP.neural_units  # number of neural units
        self.hyst = 0.5  # Neural hysteresis
        
        self.sym_avb = NP.symmetric_avb # if AVB currents should be symmetric
        self.i_on = NP.avb  # AVB input current (makes the model go)

        self.i_on_d = NP.avb_d  # AVB input current for dorsal side
        self.i_on_v = NP.avb_v  # AVB input current for ventral side



        assert self.nseg % self.n_units == 0, 'N must be divisible by neural_units'

        # GJ coupling strength
        self.i_coupling = 0.0  # Optional gap junction coupling between adjacent neurons (has virtually no effect, not usually used)

        # Set up neuromuscular junctions
        self.nmj_weight = np.zeros(self.nseg)

        # self.nmj_weight[i] = 0.7 * (1.0 - i * 0.6 / self.nseg)
        for i in range(self.nseg):
            self.nmj_weight[i] = NP.muscle_start * (1.0 - i * NP.muscle_start / self.nseg)  # Decreasing gradient in NMJ strength / muscle efficacy

        self.nmj_weight[0] = self.nmj_weight[0] / 1.5  # Helps to prevent excessive bending of head

        # Neural state variables
        self.state = np.zeros((self.n_units, 2))

        # Initialise with all neurons on one side ON
        for i in range(self.n_units):
            self.state[i][0] = 1
            self.state[i][1] = 0

        # Stretch receptor variables
        self.i_sr_d = np.zeros(self.n_units)
        self.i_sr_v = np.zeros(self.n_units)
        self.sr_weight = np.zeros(self.n_units)
        self.n_sr = 6  # This refers to the number of units (not segments) that each unit receives feedback from (thus 1 means just local feedback)
        self.n_seg_per_unit = int(self.nseg/self.n_units)

        # sr_weight is a global weigting for each unit, used to get the compensate for curvature gradient induced by the NMJ gradient above
        for i in range(self.n_units):
            self.sr_weight[i] = 0.65 * (0.4 + 0.08 * i)*(self.n_units/12.0)*(2.0/self.n_seg_per_unit)

        #calculate width of each segment
        self.width = np.zeros(self.nseg+1)
        d = 0.00008
        epsilon = 0.0000001  # epsilon is a small value which means that first and last segments will not have width 0
        for i in range(self.nseg+1):
            u = i * (1 / self.nseg)
            self.width[i] = (d/2) * (2*np.sqrt((epsilon + u) * (epsilon + 1.0 - u))/(1 + 2*epsilon))

        self.sr_shape_compensation = np.zeros(self.nseg)
        for i in range(self.nseg):
            self.sr_shape_compensation[i] = d/self.width[i]

    def update_neurons(self):
        # Add up stretch receptor contributions from all body segments in receptive field for each neural unit
        for i in range(self.n_units - self.n_sr + 1):
            self.i_sr_d[i] = 0.0
            self.i_sr_v[i] = 0.0
            for j in range(self.n_sr):
                for k in range(self.n_seg_per_unit):  # slight change from original
                    self.i_sr_d[i] += self.i_sr[(i + j) * self.n_seg_per_unit + k, 0]
                    self.i_sr_v[i] += self.i_sr[(i + j) * self.n_seg_per_unit + k, 1]

        # For units near the tail, fewer segments contribute (because the body ends)
        tmp_n_sr = self.n_sr
        for i in range(self.n_units - self.n_sr + 1, self.n_units):
            tmp_n_sr -= 1
            self.i_sr_d[i] = 0.0
            self.i_sr_v[i] = 0.0
            for j in range(tmp_n_sr):
                for k in range(self.n_seg_per_unit):  # slight change from original
                    self.i_sr_d[i] += self.i_sr[(i + j) * self.n_seg_per_unit + k, 0]
                    self.i_sr_v[i] += self.i_sr[(i + j) * self.n_seg_per_unit + k, 1]
                    
        # Compensate for the posterior segments with shorter processes
        for i in range(self.n_units - self.n_sr + 1, self.n_units):
            self.i_sr_d[i] *= np.sqrt(-(self.n_sr / (i - self.n_units)))
            self.i_sr_v[i] *= np.sqrt(-(self.n_sr / (i - self.n_units)))

        # Variables for total input current to each B-Class motorneuron
        i_d = np.zeros(self.n_units)
        i_v = np.zeros(self.n_units)

        # Current bias to compensate for the fact that neural inhibition only goes one way
        i_bias = 0.5

        # Combine AVB current, stretch receptor current, neural inhibition and bias
        for i in range(self.n_units):
            # If AVB is not symmetric
            if not self.sym_avb:
                i_d[i] = self.i_on_d + self.sr_weight[i] * self.i_sr_d[i]  # Use dorsal AVB input here
                i_v[i] = (i_bias - self.state[i, 0]) + self.i_on_v + self.sr_weight[i] * self.i_sr_v[i]  # Use ventral AVB input here
            else:
                i_d[i] = self.i_on + self.sr_weight[i] * self.i_sr_d[i]
                i_v[i] = (i_bias - self.state[i, 0]) + self.i_on + self.sr_weight[i] * self.i_sr_v[i]





        # Add gap junction currents if they are being used (typically i_coupling = 0)
        i_d[0] += (self.state[1, 0] - self.state[0, 0]) * self.i_coupling
        i_v[0] += (self.state[1, 1] - self.state[0, 1]) * self.i_coupling

        for i in range(1, self.n_units - 1):
            i_d[i] += ((self.state[i+1, 0] - self.state[i, 0]) + (self.state[i-1, 0] - self.state[i, 0]))*self.i_coupling
            i_v[i] += ((self.state[i + 1, 1] - self.state[i, 1]) + (self.state[i - 1, 1] - self.state[i, 1])) * self.i_coupling

        i_d[self.n_units-1] += (self.state[self.n_units-2, 0] - self.state[self.n_units-1, 0])*self.i_coupling
        i_v[self.n_units - 1] += (self.state[self.n_units - 2, 1] - self.state[self.n_units - 1, 1]) * self.i_coupling

        # Update state for each bistable B-class neuron
        for i in range(self.n_units):
            if i_d[i] > (0.5 + self.hyst / 2.0 - self.hyst * self.state[i, 0]): #was 0.5
                self.state[i, 0] = 1
            else:
                self.state[i, 0] = 0
            if i_v[i] > (0.5 + self.hyst / 2.0 - self.hyst * self.state[i, 1]): #was 0.5
                self.state[i, 1] = 1
            else:
                self.state[i, 1] = 0
                
        for i in range(self.nseg):
            self.v_neuron[i, 0] = self.nmj_weight[i]*self.state[int(i*(self.n_units/self.nseg)), 0] - self.nmj_weight[i]*self.state[int(i*(self.n_units/self.nseg)), 1]
            self.v_neuron[i, 1] = self.nmj_weight[i] * self.state[int(i * (self.n_units / self.nseg)), 1] - self.nmj_weight[i] * self.state[int(i * (self.n_units / self.nseg)), 0]


    def update_stretch_receptors(self, alpha):
        l_seg = 0.001 / self.nseg  # length of each segment at the midline

        current_seg = 0
        for a in alpha:
            r = (1 / abs(a)) / 1000  # convert curvature to radius
            theta = l_seg / r  # angle at the centre
            if a < 0:  # if curvature is negative, shorter side is ventral
                self.l_sr[current_seg, 1] = theta * (r - self.width[current_seg])
                self.l_sr[current_seg, 0] = theta * (r + self.width[current_seg])
            else:  # otherwise, shorter side is dorsal
                self.l_sr[current_seg, 0] = theta * (r - self.width[current_seg])
                self.l_sr[current_seg, 1] = theta * (r + self.width[current_seg])
            current_seg += 1

	#calculate input to stretch receptors
        for i in range(self.nseg):
            if self.l_sr[i][0] > l_seg:
                compensate = 0.8
            else:
                compensate = 1.2
            self.i_sr[i][0] = self.sr_shape_compensation[i] * (self.l_sr[i][0] - l_seg) / (l_seg * compensate)
            self.i_sr[i][1] = self.sr_shape_compensation[i] * (self.l_sr[i][1] - l_seg) / (l_seg)

    # based on the following paper:
    # Denham Jack E., Ranner Thomas and Cohen Netta 2018
    # Signatures of proprioceptive control in Caenorhabditis elegans locomotion
    # Phil. Trans. R. Soc. B3732018020820180208
    # http://doi.org/10.1098/rstb.2018.0208
    # def update_muscles(self, alpha):
    #     t_muscle = 0.1 / self.dt
    #     for i in range(self.nseg):
    #         dv = (self.v_neuron[i][0] - self.v_muscle[i][0])/0.1
    #         self.v_muscle[i][0] += dv*self.dt
    #         dv = (self.v_neuron[i][1] - self.v_muscle[i][1])/0.1
    #         self.v_muscle[i][1] += dv*self.dt
    #         activation = self.v_muscle[i][0] - self.v_muscle[i][1]
    #         alpha[i] += (-alpha[i] + (self.alpha0*activation))/t_muscle
    #     return alpha


    def update_muscles(self, alpha):
        t_muscle = 0.01 / self.dt
        t_muscle = 0.1
        bias_factor = 1  # Slightly more than 1 to introduce a bias towards the first muscle
        bias_constant = -0.0  # A small constant bias to further favor the first muscle
        for i in range(self.nseg):
            dv = (self.v_neuron[i][0] - self.v_muscle[i][0])/t_muscle
            self.v_muscle[i][0] += dv*self.dt
            dv = (self.v_neuron[i][1] - self.v_muscle[i][1])/t_muscle
            self.v_muscle[i][1] += dv*self.dt
            activation = (self.v_muscle[i][0] * bias_factor + bias_constant) - self.v_muscle[i][1]
            alpha[i] += (-alpha[i] + (self.alpha0*activation)) * t_muscle
        return alpha
    
    # def update_muscles(self, alpha):
    #     t_muscle = 0.1 / self.dt
    #     bias_factor = 2  # Slightly more than 1 to introduce a bias towards the second muscle
    #     bias_constant = 0.01  # A small constant bias to further favor the second muscle
    #     for i in range(self.nseg):
    #         dv = (self.v_neuron[i][0] - self.v_muscle[i][0])/0.1
    #         self.v_muscle[i][0] += dv*self.dt
    #         dv = (self.v_neuron[i][1] - self.v_muscle[i][1])/0.1
    #         self.v_muscle[i][1] += dv*self.dt
    #         activation = self.v_muscle[i][0] - (self.v_muscle[i][1] * bias_factor + bias_constant)
    #         alpha[i] += (-alpha[i] + (self.alpha0*activation))/t_muscle
    #     return alpha



    def update_all(self, alpha):
        self.update_stretch_receptors(alpha)
        self.update_neurons()
        return self.update_muscles(alpha)


# bottom n segments will be assigned this circuit

# this will contain the circuit for the worm, used for turning
class HeadAndNeckCircuit(NeuralModel):
    pass
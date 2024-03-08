# this contains an environment for a worm to be in 
# create a parameter e.g. gravity, concentration which has a mesh, defined by a lambda function
# create as many as u want
# given an x,y coordinate return the parameters at that point


# need to store the function somehere
class Environment:
    def __init__(self):
        # Initialize an empty dictionary to hold parameter name -> lambda function mappings
        self.parameters = {}

    def add_parameter(self, name, func):
        # Add a new parameter with its associated function
        self.parameters[name] = func

    def get_parameters_at(self, x, y):
        # Given x, y coordinates, return a dictionary of parameter values at that point
        return {name: func(x, y) for name, func in self.parameters.items()}

    def get_parameter_func(self, name):
        return self.parameters[name]
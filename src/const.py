import numpy as np

# Those global constants will be used directly by the solver.
H_BAR = 1.0
M = 1.0

X_MIN = -10
X_MAX = 10
N_X   = 101

Y_MIN = -10
Y_MAX = 10
N_Y   = 101

T_MAX = 10
DT_FTCS = 0.02 / 800
DT_BTCS = 0.02 / 40
DT_CTCS = 0.02 / 4

# Those specific constants are available parameters for the wave function in the
# configuration file. Use the name of a constant instead of a numeric value in
# the JSON file to use a specific value (example: 1 / sqrt(2 * pi)).
CONSTANTS = {
    # "NAME": VALUE,
    "A": 1 / np.sqrt(2 * np.pi),
}

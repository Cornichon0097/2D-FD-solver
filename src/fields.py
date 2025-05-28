import numpy as np

from const import *


def youngs_slits():
    """
    return the potential field for the young's slits simulation
    """
    v0 = np.zeros((N_X, N_Y), dtype = np.float64)

    for i in range(N_X):
        for j in range(N_Y):
            if j == (N_Y // 2):
                v0[i, j] = 50
    
    for i in range(N_X):
        for j in range(N_Y):
            if i == (N_X // 2):
                for gap in range(1, 2):
                    v0[i - gap, j] = v0[i + gap, j] = 0

    return v0


def barrier():
    """
    return the potential field for the barrier simulation
    """
    v0 = np.zeros((N_X, N_Y), dtype = np.float64)

    for i in range(N_X):
        for j in range(N_Y):
            if j == (N_Y // 2):
                v0[i, j] = 10

    return v0


def potential_2D_HO():
    """ 
    return the potential field for the 2D_H0 simulation
    """
    X = np.linspace(X_MIN, X_MAX, N_X)
    Y = np.linspace(Y_MIN, Y_MAX, N_Y)

    v0 = np.zeros((N_X, N_Y), dtype = np.float64)

    for x in range(len(X)):
        for y in range(len(Y)):
            v0[x, y] = (1 / 9) * (X[x] ** 2 + Y[y] ** 2)

    return v0

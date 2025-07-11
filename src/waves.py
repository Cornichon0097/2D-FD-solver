""" @package waves.py
Provides wave functions for the solver.
"""
import numpy as np

from const import *


def gaussian(x0, y0, w, A, kx, ky):
    """ Gaussian wave function.

    @param x0 the initial x position,
    @param y0 the initial y position,
    @param w  the width of the gaussian,
    @param A  the normalization constant,
    @param kx the initial x speed,
    @param ky the initial y speed.
    """
    X = np.linspace(X_MIN, X_MAX, N_X)
    Y = np.linspace(Y_MIN, Y_MAX, N_Y)

    psi = np.zeros((N_X, N_Y), dtype = complex, order = 'F')

    for x in range(len(X)):
        for y in range(len(Y)):
            psi[x, y] = A * np.exp(1j * (kx * X[x] + ky * Y[y])) * np.exp(-(((X[x] - x0) ** 2 + (Y[y] - y0) ** 2) / (w ** 2)))

    return psi

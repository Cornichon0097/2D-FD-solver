import numpy as np
import time

import solver


X_MIN = -10
X_MAX = 10
N_X   = 101

Y_MIN = -10
Y_MAX = 10
N_Y   = 101

DT = 0.02 / 800


def gaussian(x0, y0, w, A, kx, ky):
    X = np.linspace(X_MIN, X_MAX, N_X)
    Y = np.linspace(Y_MIN, Y_MAX, N_Y)

    psi = np.zeros((N_X, N_Y), dtype = complex, order = 'F')

    for x in range(len(X)):
        for y in range(len(Y)):
            psi[x, y] = A * np.exp(1j * (kx * X[x] + ky * Y[y])) * np.exp(-(((X[x] - x0) ** 2 + (Y[y] - y0) ** 2) / (w ** 2)))

    return psi


def potential_2D_HO():
    X = np.linspace(X_MIN, X_MAX, N_X)
    Y = np.linspace(Y_MIN, Y_MAX, N_Y)

    v0 = np.zeros((N_X, N_Y), dtype = np.float64)

    for x in range(len(X)):
        for y in range(len(Y)):
            v0[x, y] = (1 / 9) * (X[x] ** 2 + Y[y] ** 2)

    return v0


def main():
    psi = gaussian(0, 0, 2.06, 1 / np.sqrt(2 * np.pi), 0, 0)
    V0  = potential_2D_HO()

    solv = solver.Solver(np.asfortranarray(V0), np.asfortranarray(np.real(psi)),
                         np.asfortranarray(np.imag(psi)), 1.0, 1.0, "ftcs",
                         (X_MAX - X_MIN) / N_X, (Y_MAX - Y_MIN) / N_Y, DT)

    begin = time.time()

    for i in range(0, 10):
        solv.compute()
        psi = solv.r_part() + 1j * solv.i_part()
        print(np.linalg.norm(psi))

    end = time.time()

    print("Calculation terminated, time elapsed: %f" % (end - begin))


if __name__ == "__main__":
    main()

import numpy as np
import pickle

import solver

V0    = np.zeros((10,10), dtype=np.float64, order='F')
rpart = np.zeros((10,10), dtype=np.float64, order='F')
ipart = np.zeros((10,10), dtype=np.float64, order='F')

solv = solver.Solver(V0, rpart, ipart, "ftcs", 1.0, 1.0, 1.0)

for i in range(1, 10):
    solv.compute()
    print({pickle.dumps(solv.r_part() + 1j * solv.i_part())})

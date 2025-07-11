""" @package monitor.py
Provides a monitor for the solver.

The monitor is in charge to run the solver and make sure no problem occurs.
"""
import sys

import bson
import pickle

import logging

import time

import numpy as np
import matplotlib.pyplot as plt

from mongoDBConnection import MongoDBConnection

import fieldGenerator
import postProcessor
import solver

from const import *


def connect_db(mongodb):
    """ Creates connection with MongoDB.

    @param mongodb the MongoDB instance.

    @return the MongoDB connection.
    """
    db = MongoDBConnection(mongodb['host'], mongodb['username'],
                           mongodb['password'], mongodb['dbname'])
    db.use(mongodb['dbname'], mongodb['collection'])

    return db


def extract(data):
    """ Extracts data from a MongoDB document.

    @param data the MongoDB document.

    @return the data extracted.
    """
    res = [
        data['checksum'],
        pickle.loads(data['v0']),
        pickle.loads(data['psi']),
        np.asfortranarray(np.real(pickle.loads(data['psi']))),
        np.asfortranarray(np.imag(pickle.loads(data['psi']))),
        data['scheme'],
        data['span'],
    ]

    return res


def compute(db, checksum, v0, psi, r_part, i_part, scheme, span):
    """ Runs the solver.

    The compute() function runs the solver and saves results in \a db.

    @param db       the database connection,
    @param checksum the run checksum,
    @param v0       the initial field,
    @param psi      psi
    @param r_part   real part of psi,
    @param i_part   imaginair part of psi,
    @param scheme   the scheme,
    @param span     the span between insert in database.
    """
    if scheme == "ftcs":
        dt = DT_FTCS
    elif scheme == "btcs":
        dt = DT_BTCS
    elif scheme == "ctcs":
        dt = DT_CTCS

    solv = solver.Solver(np.asfortranarray(v0), r_part, i_part, H_BAR, M, scheme,
                         (X_MAX - X_MIN) / N_X, (Y_MAX - Y_MIN) / N_Y, dt)

    logging.info("Norm: %f" % (np.linalg.norm(psi)))

    t     = 0
    count = 0
    V0    = pickle.dumps(v0)

    begin = time.time()

    while t <= T_MAX:
        solv.compute()
        t = t + dt
        count = count + 1

        if count >= span:
            psi = solv.r_part() + 1j * solv.i_part()
            logging.debug("Norm: %f" % (np.linalg.norm(psi)))
            db.insert({"checksum": checksum, "v0": V0,
                       "psi": pickle.dumps(psi), "norm": np.linalg.norm(psi),
                       "scheme": scheme, "span": span})
            count = 0

    end = time.time()

    logging.info("Calculation terminated, time elapsed: %f" % (end - begin))
    logging.info("Norm: %f" % (np.linalg.norm(psi)))


def run(mongodb, param_file):
    """ Monitor main function.

    @param mongodb    the MongoDB instance,
    @param param_file the path to the parameters file.
    """
    print("Initialisation...")

    db = connect_db(mongodb)
    logging.debug("MongoDB initialised")

    run_id = fieldGenerator.generate(param_file, db)
    logging.debug("Field initialised")

    document = db.retrieve()
    data     = extract(document)

    if run_id == None:
        postProcessor.generate_init_vti(data[1], data[3], data[4])

        print("Initial VTK generated in vti/")
        c = input("Continue? [Y/n] ")

        if c != "Y":
            print("Aborting")
            db.insert({"checksum": None})
            sys.exit(0)
    else:
        print("Restarting previous run...")
        logging.info("Previous run interrupted, restarting...")

    print("Calculating...")
    logging.info("Starting simulation")

    compute(db, *data)
    logging.debug("Compute terminated")

    print("Generating VTK...")

    count = 0

    for i in db.retrieve_all({"checksum": document['checksum']}):
        data = extract(i)
        postProcessor.generate_vti(data[1], data[3], data[4], count)
        count = count + 1

    db.insert({"checksum": None})

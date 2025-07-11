""" @package fieldGenerator
Provides the field generator for the solver.

The fieldGenerator package sets initial states and field for the solver. If the
previous run has been interrupted, then the field generator will reload it.
"""
import json
import bson
import pickle

import hashlib
import gridfs

import logging

import numpy as np
import matplotlib.pyplot as plt

from mongoDBConnection import MongoDBConnection
import pymongo.errors

from const import *
import fields
import waves


def hash_content(content):
    """ Returns a human readable hash.

    @param content the hashed content.

    @return content as a human readable hash.
    """
    m = hashlib.md5()

    m.update(content)

    return m.hexdigest()


def init_states(config):
    """ Initializes psi and V0

    The init_states() function returns psi and V0 initialized with \a config.

    @param config the initial configuration.

    @return initial psi and V0.
    """
    args = []
    i = 0

    for arg in config['args']:
        if type(arg) == str:
            args.append(CONSTANTS[arg])
        else:
            args.append(arg)

        i = i + 1

    if config['type'] == "fun":
        v0 = getattr(fields, config['field'])()
    else:
        v0 = getattr(fields, config['field'])

    psi = getattr(waves, config['wave'])(*args)

    return psi, v0


def generate(param_file, db):
    """ Puts initial states in database.

    The generate() function generates initial states defined in \a param_file
    and puts it in \a db. If a previous run was interrupted and parameters match
    with \a param_file, then this function retuns the latest result found in
    \a db instead.

    @param param_file the parameters file,
    @param db         the database.

    @return true if a previous run can be restarted, false otherwise.
    """
    document = db.retrieve()

    if document != None:
        if document['checksum'] != None:
            logging.info("Checksum from previous run found")
            return document['checksum']

    with open(param_file, "r") as read_file:
        solver = json.load(read_file)

    psi, v0 = init_states(solver)
    logging.debug("Initiale states set")

    checksum = (str(solver) + str(psi) + str(v0)).encode("utf-8")

    db.insert({"checksum": hash_content(checksum),
               "v0": bson.binary.Binary(pickle.dumps(v0, protocol = 2)),
               "psi": pickle.dumps(psi), "norm": np.linalg.norm(psi),
               "scheme": solver['scheme'], "t": 0, "span": solver['span']})
    logging.info("Initiale states inserted in the DB")

""" @package fieldGenerator
Provides the field generator for the solver.

The fieldGenerator package set initial states and field for the solver. If the
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

    The hash_content() function a human readable hash.

    @param content the hashed content.

    @return content as a human readable hash.
    """
    m = hashlib.md5()

    m.update(content)

    return m.hexdigest()


def init_states(config):
    """ Initialise psi and V0

    The init_states() function initialise psi and V0 With \a config paramèters.

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


def generate(config_file, db):
    """ Puts initial states in database.

    The generate() function generates and puts initial states in the database.
    If needed, the generate() function can return the latest result of a
    previous run to restart it.

    @param config_file the configuration file,
    @param db          the database.

    @return true if a previous run can be restarted, false otherwise.
    """
    document = db.retrieve()

    if document != None:
        if document['checksum'] != None:
            logging.warning("Checksum from previous run found")
            return document['checksum']

    with open(config_file, "r") as read_file:
        solver = json.load(read_file)

    psi, v0 = init_states(solver)
    logging.debug("Initiale states set")

    checksum = (str(solver) + str(psi) + str(v0)).encode("utf-8")

    db.insert({"checksum": hash_content(checksum),
               "v0": bson.binary.Binary(pickle.dumps(v0, protocol = 2)),
               "psi": pickle.dumps(psi), "norm": np.linalg.norm(psi),
               "scheme": solver['scheme'], "span": solver['span']})
    logging.info("Initiale states inserted in the DB")

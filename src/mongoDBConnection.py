""" @package MongoDBConnection
Provides a MongoDB client interface.

The MongoDBconnection is an interface that provides simple utilities to
interact with a MongoDB database.
"""
from pymongo import MongoClient
import pymongo.errors

from bson.objectid import ObjectId

import logging


class MongoDBConnection:
    """ MongoDBConnection class.

    The MongoDBConnection class is an opaque object which establish connection
    to a MongoDB server. It provides basic methods to insert or retrieve
    documents from the database.
    """

    """ The MongoDB client connection. """
    client = None

    """ The MongoDB client database. """
    db = None

    """ The MongoDB client collection. """
    collection = None


    def __init__(self, host, username, password, dbname):
        """ MongoDBConnection constructor.

        The MongDBConnection constructor creates a connection to MongoDB.

        @param self     the object pointer,
        @param host     the MongoDB host,
        @param username the user login,
        @param password the user password,
        @param dbname   the MongoDB database.
        """
        self.client = MongoClient("mongodb://%s:%s@%s/%s"
                                  % (username, password, host, dbname))
        logging.info("Connected to mongodb://%s:%s@%s/%s"
                     % (username, password, host, dbname))


    def use(self, dbname, collection):
        """ Sets the database and the collection to use.

        The use() method sets the database \a dbname and the collection
        \a collection to use for MongoDB transactions.

        @param self       the object pointer,
        @param dbname     the database name,
        @param collection a collection of the database.
        """
        try:
            self.db = self.client[dbname]
            self.collection = self.db[collection]
            logging.info("Switched to DB %s collection %s"
                         % (self.db.name, self.collection.name))
        except pymongo.errors.OperationFailure as e:
            logging.error("Can’t switch to DB %s collection %s: %s"
                          % (dbname, collection, str(e)))


    def insert(self, data):
        """ Insterts a new document.

        The insert() method inserts the new document \a data in the curent
        collection set by the use() method.

        @see use()

        @param self the object pointer,
        @param data the new document.

        @return the ID of the new document.
        """
        data_id = None

        try:
            data_id = self.collection.insert_one(data).inserted_id
            logging.debug("Inserted document %s" % (str(data_id)))
            self.last = data_id
        except pymongo.errors.OperationFailure as e:
            logging.error("Insertion failed: %s" % (str(e)))

        return data_id


    def retrieve(self, data = None):
        """ Retrieves a document.

        The retrieve() method retrieves one document that matchs \a data filter
        in the current collection set by the use() method. If no filter is
        specified, then the retrieve() method returns the last insterted
        documment in the database.

        @see use()

        @param self the object pointer,
        @param data the parameters for retrievement.

        @return the document retrieved.
        """
        document = None

        try:
            if data != None:
                res = self.collection.find(data).sort("_id", -1).limit(1)
            else:
                res = self.collection.find().sort("_id", -1).limit(1)

            for document in res:
                break

            if document != None:
                logging.debug("Retrieved document %s" % (str(document['_id'])))
        except pymongo.errors.OperationFailure as e:
            logging.error("Retrieve failed: %s" % (str(e)))

        return document


    def retrieve_all(self, data = None):
        """ Retrieves all documents.

        The retrieve_all() methode retrieves all documents in the current
        collection set by the use() method.

        @see use()

        @param self the object pointer.

        @return all documents retrieved.
        """
        documents = None

        try:
            if data == None:
                documents = self.collection.find()
            else:
                documents = self.collection.find(data)

            logging.debug("Retrieved all documents")
        except pymongo.errors.OperationFailure as e:
            logging.error("Retrieve failed: %s" % (str(e)))

        return documents

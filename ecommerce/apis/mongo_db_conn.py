from pymongo import MongoClient

class MongoConnection(object):
    def __init__(self):
        self._host = 'localhost'
        self._port = 27017
        self._db = 'ecommerce'
    
    def mongodbconn(self):
        client =  MongoClient(self._host,self._port)
        db_conn = client[self._db]
        return db_conn



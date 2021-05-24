"""
Class variables for database (insert/delete)
"""
from pymongo import MongoClient

class Mongo:
    def __init__(self, tester="tester"):
        self.tester = tester
        self.client = None
        self.db = None

    def mk_db(self, dataB):
        self.db = self.client[dataB]

    def connect(self):
        self.client = MongoClient('mongodb://' + self.tester, 27017)
        # Default mongoDB Port

    def insert_o(self, data_b):
        self.db[collection].insert_one(data_b)
        # insert_one function
        # credit : https://docs.mongodb.com/manual/reference/method/db.collection.insertOne/
    def delete_all(self, collection):
        self.db[collection].delete_many({})

    def list_all(self, collection):
        return list(self.db[collection].find())
        # return all the list that is contained in db

"""
Class variables for database (insert/delete)
"""
from pymongo import MongoClient

class Mongo:
    def __init__(self, tester="tester"):
        self.tester = tester
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient('mongodb://' + self.client_name, 27017)
        # Default mongoDB Port

    def mk_db(self, dataB):
        self.db = self.client[dataB]

    def insert_o(self, collection, row):
        self.db[collection].insert_one(row)
        # insert_one function
        # credit : https://docs.mongodb.com/manual/reference/method/db.collection.insertOne/
    def delete_all(self, collection):
        self.db[collection].delete_many({})

    def list_all(self, collection):
        return list(self.db[collection].find())

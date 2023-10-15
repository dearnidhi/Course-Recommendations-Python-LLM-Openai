from pymongo import MongoClient

def get_database_connection():
    client = MongoClient('localhost', 27017)
    db = client['course']
    return db

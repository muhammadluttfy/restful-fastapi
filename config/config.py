import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database("dev_restful-fastapi")

def get_db_connection():
  return db
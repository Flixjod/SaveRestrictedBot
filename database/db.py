from pymongo import MongoClient
from config import DB_URI

mongo_client = MongoClient(DB_URI)
database = mongo_client.restricted_save
users_collection = database['users']
sessions_collection = database['sessions']

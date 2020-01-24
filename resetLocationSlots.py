# Connection
import pymongo
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://mustajabhannan:Hannan786@cluster0-n7aqf.mongodb.net/test?retryWrites=true&w=majority"
)

db = cluster["attendance"]
collection = db["locations"]

def resetAttendanceSlot():
    locations = collection.find({})
    for location in locations:
        id = location['locationID']
        minimum_slots = location['minimum']
        collection.update({"locationID": id}, {"$set": {"available_spots": minimum_slots}})
        return True
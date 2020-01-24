# Connection
import pymongo
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://mustajabhannan:Hannan786@cluster0-n7aqf.mongodb.net/test?retryWrites=true&w=majority")

db = cluster["attendance"]
collection = db["locations"]


class Location:

    def __init__(self, loc_id):
        self.loc_id = loc_id

    def addLocation(self, name, minimum, maximum):

        """Returns True if the data is added successfully."""
        if (minimum > maximum):

            print("Minimum Days Cant be More Than Maximum Days")

        else:

            self.name = name
            self.minimum = int(minimum)
            self.maximum = int(maximum)

            findRecord = collection.find(
                {
                    "locationID": self.loc_id
                }

            )
            findRecord = list(findRecord)

            if findRecord == []:
                data = {
                    "locationID": self.loc_id,
                    "locationName": self.name,
                    "minimum": self.minimum,
                    "maximum": self.maximum,
                    "available_spots": self.minimum
                }
                result = collection.insert_one(data)

                if result.acknowledged is True:
                    return True
                else:
                    print ("Failed to acknowledge")
                    return False
            else:
                return "Record Already Exists"

    def addGPS(self, latitude, longitude):

        data = {
            "latitude": latitude,
            "longitude": longitude
        }
        insert = collection.update(
            {"locationId": self.loc_id},
            {"$set": data},
            upsert=True
        )

        return "Inserted GPS"

    def resetSpots(self):
        """
        Reset the available spots field in the database when the minimum spots are completely filled.
        :return:
        """

        try:
            findRecord = list(collection.find(
                {
                    "locationID": self.loc_id
                }))

            # Change available spots in minimum is finished.
            if findRecord[0]['available_spots'] == 0:
                insert = collection.update(
                    {"locationID": self.loc_id},
                    {"$set":
                         {"available_spots": (findRecord[0]['maximum'] - findRecord[0]['minimum'])}
                     }

                )
            return True
        except Exception as e:
            print(e)

    def resetAttendanceSlot(self):
        locations = collection.find({})
        for location in locations:
            id = location['locationID']
            minimum_slots = location['minimum']
            collection.update({"locationID":id},{"$set":{"available_spots":minimum_slots}})



def getAll():
    data = collection.find()
    return data


import pymongo
activeDatabase = 'saiRecords'
connection = pymongo.MongoClient("localhost", 27017)
database = connection[activeDatabase]
collection = database['inventory']

a=collection.find()
for x in a:
    print(a)
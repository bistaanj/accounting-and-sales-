import pymongo
connection = pymongo.MongoClient("localhost", 27017)
database = connection['saiRecords']
collection = database['panDetails']

r = {'_id':"123456789", 'Name': ' Anuj Bista', 'Phone Number':1234567890}
    
collection.insert_one(r)
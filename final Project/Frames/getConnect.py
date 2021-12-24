import pymongo
def getConnect(database,collection):
    connection = pymongo.MongoClient('localhost',27017)
    # database = connection['saiRecords']
    database = connection[database]
    # collection = database['inventory']
    collection = database[collection]

    return collection

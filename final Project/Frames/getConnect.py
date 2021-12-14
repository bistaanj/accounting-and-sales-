import pymongo
def getConnect(self):
    # client = MongoClient("mongodb+srv://rootUser:clouddbaccess@trialdbs.i4jhu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    # db = client.get_database('saiRecords')
    # collection = db.inventory
    connection = pymongo.MongoClient('localhost',27017)
    database = connection['saiRecords']
    collection = database['inventory']
    return collection

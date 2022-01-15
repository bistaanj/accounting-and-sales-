from bson.objectid import ObjectId
from Frames.supportingFunctions import getConnect
from datetime import datetime


def manageStock(id, quantity, sp, activeDatabase):
    # connection = pymongo.MongoClient("localhost", 27017)
    # database = connection[activeDatabase]
    # collection = database['presentStock']
    # connection = pymongo.MongoClient("localhost", 27017)
    # database = connection[activeDatabase]
    collection = getConnect(activeDatabase, 'presentStock')
    a = quantity
    ref_id = id
    q = collection.find_one({'_id': ObjectId(ref_id)})
    oq = (q['Stock'][-1]['Quantity'])
    oc = q['Stock'][-1]['CP']
    nw = datetime.now()
    id = nw.strftime("%d%m%Y-%H%M%S")
    rawdata = []
    # collection.update_one({'_id': ObjectId(ref_id)}, {'$push':{'Stock':{'Quantity':600,'CP':50}}})
    while(a != 0):
        innerDict = {}
        if (oq < a):
            innerDict['Quantity'] = oq
            innerDict['CP'] = oc
            innerDict['SP'] = sp
            rawdata.append(innerDict)
            a = a - oq
            collection.update_one({'_id': ObjectId(ref_id)}, {
                                  '$pop': {'Stock': 1}})
            q = collection.find_one({'_id': ObjectId(ref_id)})
            oq = (q['Stock'][-1]['Quantity'])
            oc = q['Stock'][-1]['CP']
        else:

            newValue = oq - a

            innerDict['Quantity'] = a
            innerDict['CP'] = oc
            innerDict['SP'] = sp
            rawdata.append(innerDict)
            a = 0
            collection.update_one({'_id': ObjectId(ref_id)}, {
                                  '$pop': {'Stock': 1}})
            collection.update_one({'_id': ObjectId(ref_id)}, {
                                  '$push': {'Stock': {'Quantity': newValue, 'CP': oc}}})
    collection = getConnect(activeDatabase, 'outStock')
    collection.find_one_and_update(
        {'_id': ObjectId(ref_id)}, {'$set': {id: rawdata}})

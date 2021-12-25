import pymongo
from bson.objectid import ObjectId
from datetime import datetime
connection = pymongo.MongoClient("localhost", 27017)
database = connection['saiRecords']
collection = database['presentStock']


def manageStock(id, quantity):
    connection = pymongo.MongoClient("localhost", 27017)
    database = connection['saiRecords']
    collection = database['presentStock']
    a = quantity
    ref_id = id
    q=collection.find_one({'_id':ObjectId(ref_id)}) 
    for x in q['Stock']:
        print(x)
    oq =(q['Stock'][-1]['Quantity'])
    oc = q['Stock'][-1]['CP']
    print(" oq, oc")
    print(oq, oc )
    nw = datetime.now()
    id = nw.strftime("%d%m%Y-%H%M%S")
    rawdata=[]
    # collection.update_one({'_id': ObjectId(ref_id)}, {'$push':{'Stock':{'Quantity':600,'CP':50}}})
    while(a != 0):
        innerDict={}
        if (oq< a):
            innerDict['Quantity']= oq
            innerDict['CP']= oc
            rawdata.append(innerDict)
            a = a - oq
            collection.update_one({'_id':ObjectId(ref_id)}, {'$pop': {'Stock': 1 } } )
            q=collection.find_one({'_id':ObjectId(ref_id)}) 
            oq =(q['Stock'][-1]['Quantity'])
            oc = q['Stock'][-1]['CP']
        else:
            newValue = oq - a
            innerDict['Quantity']= newValue
            innerDict['CP']= oc
            rawdata.append(innerDict)
            a=0
            collection.update_one({'_id':ObjectId(ref_id)}, {'$pop': {'Stock': 1 } } )
            collection.update_one({'_id': ObjectId(ref_id)}, {'$push':{'Stock':{'Quantity':newValue,'CP':oc}}})
    collection = database['outStock']
    collection.update_one({'_id':ObjectId(ref_id)},{id:rawdata})
    
    
        
# a=(q.Stock)
# print(a[0])

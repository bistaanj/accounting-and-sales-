import pymongo
from bson.objectid import ObjectId
connection = pymongo.MongoClient("localhost", 27017)
database = connection['saiRecords']
collection = database['presentStock']

def manageStock(id, quantity):
    a = quantity
    ref_id = id
    q=collection.find_one({'_id':ObjectId(ref_id)}) 
    oq =(q['Stock'][-1]['Quantity'])
    oc = q['Stock'][-1]['CP']
    print(" oq, oc")
    print(oq, oc )
    while(a != 0):
        if (oq< a):
            a = a - oq
            collection.update_one({'_id':ObjectId(ref_id)}, {'$pop': {'Stock': 1 } } )
            q=collection.find_one({'_id':ObjectId(ref_id)}) 
            oq =(q['Stock'][-1]['Quantity'])
            oc = q['Stock'][-1]['CP']
        else:
            newValue = oq - a
            a=0
            collection.update_one({'_id':ObjectId(ref_id)}, {'$pop': {'Stock': 1 } } )
            collection.update_one({'_id': ObjectId(ref_id)}, {'$push':{'Stock':{'Quantity':newValue,'CP':oc}}})
            
    q=collection.find_one({'_id':ObjectId(ref_id)}) 
    
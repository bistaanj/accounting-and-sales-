import pymongo
from bson.objectid import ObjectId
connection = pymongo.MongoClient("localhost", 27017)
database = connection['saiRecords']
collection = database['presentStock']
a = 130
# 
def manageStock(id, quantity):
    a = quantity
    ref_id = id
    q=collection.find_one({'_id':ObjectId(ref_id)}) 
    for x in q['Stock']:
        print(x)
    oq =(q['Stock'][-1]['Quantity'])
    oc = q['Stock'][-1]['CP']
    print(" oq, oc")
    print(oq, oc )
    # collection.update_one({'_id': ObjectId(ref_id)}, {'$push':{'Stock':{'Quantity':600,'CP':50}}})
    while(a != 0):
        # a=a-1
        # print(a)
        if (oq< a):
            a = a - oq
            collection.update_one({'_id':ObjectId(ref_id)}, {'$pop': {'Stock': 1 } } )
            q=collection.find_one({'_id':ObjectId(ref_id)}) 
            oq =(q['Stock'][-1]['Quantity'])
            oc = q['Stock'][-1]['CP']
        else:
            newValue = oq - a
            a=0
            print('newValue')
            print(newValue)
            collection.update_one({'_id':ObjectId(ref_id)}, {'$pop': {'Stock': 1 } } )
            collection.update_one({'_id': ObjectId(ref_id)}, {'$push':{'Stock':{'Quantity':newValue,'CP':oc}}})
    print(' \n Updated \n')
    q=collection.find_one({'_id':ObjectId(ref_id)}) 
    for x in q['Stock']:
        print(x)


        
# a=(q.Stock)
# print(a[0])

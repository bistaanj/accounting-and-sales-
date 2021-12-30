
import pymongo
import re

def addEnterprise(name, password,dbsKey):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~: ]')
    connection = pymongo.MongoClient('localhost',27017)
    dbs = connection['enterprise']
    key = dbsKey
    collection = dbs['registeredEnterprise']
    try:
        nm = name
        ps = password
        if len(nm)== 0 or len(ps) == 0:
            raise ValueError  
        
        if (regex.search(key)==None):
            print('Accepted')
        else:
            raise ValueError 
        rawData = {}
        rawData['name']= nm 
        rawData['password']= ps
        rawData['key']= key
        
        collection.insert_one(rawData)
    except ValueError:
        return(False)
    dbs= connection[key]
    collection = dbs['configuration']
    configData= {
        "_id": "settingsData",
        "receiver_email": "gmail@gmail.com",
        "sender_email": "gmail@gmail.com",
        "sender_password": "insertPassword",
        "master_password": ps
        }
    collection.insert_one(configData)
    return(True)
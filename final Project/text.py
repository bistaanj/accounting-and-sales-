raw_data = {}
raw_data['02122021-121212']=[]
innerDict={}
innerDict['Quantity']= 10
innerDict['CP']= 30
raw_data['02122021-121212'].append(innerDict)
for x in raw_data:
    print(innerDict[x] )

innerDict['Quantity']= 20
innerDict['CP']= 60

raw_data['02122021-121212'].append(innerDict)
print("New Array")
for x in raw_data:
    print(x , innerDict[x] )
    

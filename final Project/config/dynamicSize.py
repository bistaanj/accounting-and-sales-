from datetime import datetime
from win32api import GetSystemMetrics, WinExec
import json
from Frames.supportingFunctions import getConnect
# from dynamicSize import FR, WR, HR

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

availableFonts = ['Helvetica','Times New Roman','Futura','Frutiger']
WR = width/1366
HR = height/768
FR = (width*height)/(1366*768)
dynamicSize = {
    "WidthRatio": WR,
    "HeightRatio": HR,
    "FontRatio": FR
}
Y = []
for i in range(2000,2099):
    Y.append(i)
M = ["Baisakh","Jestha","Ashar","Shrawan","Bhadra","Ashoj","Kartik","Mangsir","Poush","Magh","Falgun","Chaitra"]
D = []
nPDates = json.load(open("./config/date.json","r"))

def getFontToUse(database):
    fontToUse  =  getConnect(database,'configuration').find_one({'_id':'settingsData'})["fontToUse"]
    if (fontToUse):
        return fontToUse
    else:
        return "Helvetica"
    
def getCurrentDateType(database):
    currentDateType  =  getConnect(database,'configuration').find_one({'_id':'settingsData'})["currentDateType"]
    if (currentDateType):
        return currentDateType
    else:
        return "AD"
    
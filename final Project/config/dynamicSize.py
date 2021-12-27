from datetime import datetime
from win32api import GetSystemMetrics, WinExec
import json
# from dynamicSize import FR, WR, HR

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
fontToUse = "Helvetica"
day1Date = datetime.date(datetime.now())

WR = width/1366
HR = height/768
FR = (width*height)/(1366*768)
dynamicSize = {
    "WidthRatio": WR,
    "HeightRatio": HR,
    "FontRatio": FR
}
nepaliDate = True
Y = []
for i in range(2000,2099):
    Y.append(i)
M = ["Baisakh","Jestha","Ashar","Shrawan","Bhadra","Ashoj","Kartik","Mangsir","Poush","Magh","Falgun","Chaitra"]
D = []
nPDates = json.load(open("./config/date.json","r"))
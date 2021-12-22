from datetime import datetime
from win32api import GetSystemMetrics, WinExec
# from dynamicSize import FR, WR, HR

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
fontToUse = "Aerial"
day1Date = datetime.date(datetime.now())
WR = width/1366
HR = height/768
FR = (width*height)/(1366*768)
dynamicSize = {
    "WidthRatio": WR,
    "HeightRatio": HR,
    "FontRatio": FR
}

import xlparser as xlp
from pathlib import Path
import sys
import json

host=[]
hostsList=[]
x=[]
okips=sys.argv[1]
okipsList=okips.split(",")

xlsxFile='/usr/local/nagiosxi/html/config/uploads/FILE.xlsx'
my_file = Path("/usr/local/nagiosxi/html/config/uploads/FILE.xlsx")

if my_file.is_file():
    hosts=xlp.bulkHostCheckAsServices(xlsxFile)
    for dict in hosts:
        if dict['IP'] in okipsList:
            for key,value in dict.items():

                host.append(value)
            hostsList.append(host)
            host = []


print(hostsList)
#print(dict)





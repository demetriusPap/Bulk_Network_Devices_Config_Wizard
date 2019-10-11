import xlparser as xlp
import RESTFunctions as rf
import re
import requests as req
import sys, json
import database as db



hgalias='This host group has been created automatically by wizzard'
cgalias='This contact group has been created automatically by wizzard'
xlsxFile='/usr/local/nagiosxi/html/config/uploads/FILE.xlsx'
ci=0
hi=0


hostGroup,contactGroup=xlp.groups(xlsxFile)

for key in hostGroup.keys():
    hostgrouplist = rf.getHostGroupName(db.serverName)
    if key not in hostgrouplist:
        hi+=1
        hresult=rf.createHostGroup(key, hgalias, db.serverName)


for key in contactGroup.keys():
    contactgrouplist = rf.getContactGroupName(db.serverName)
    if key not in contactgrouplist:
        ci+=1
        cresult=rf.createContactGroup(key, cgalias, db.serverName)






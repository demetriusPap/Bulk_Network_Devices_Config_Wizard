import database as db
import RESTFunctions as rf
grouplist=[]



a=rf.getContactGroupName(db.serverName)
b=rf.getHostGroupName(db.serverName)
grouplist.append(a)
grouplist.append(b)
print(grouplist)

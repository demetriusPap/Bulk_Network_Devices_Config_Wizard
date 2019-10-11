import SSHFunctions as sf
import sys
import json
import database as db

values=[int(sys.argv[4])/100,int(sys.argv[2])/100,int(sys.argv[5])/100, int(sys.argv[3])/100]
ips=sys.argv[1]
#ips='172.16.10.96,172.16.10.181'
ipsList=ips.split(',')


for ip in ipsList:
    serviceToDoDict, sysName =sf.getActiveIntefaceList(db.serverName,ip)
    #print(ip)


    for activeInterface in serviceToDoDict.keys():
        desc = serviceToDoDict[activeInterface]['Desc']

        if int(serviceToDoDict[activeInterface]['Band']) > 999 and int(
                serviceToDoDict[activeInterface]['Band']) < 999999:
            scale = 'Kbps'
            factor = 1000
        elif int(serviceToDoDict[activeInterface]['Band']) > 999999:
            scale = 'Mbps'
            factor = 1000000
        else:
            scale = 'bps'
            factor = 1

        scaledValues = [int(serviceToDoDict[activeInterface]['Band']) * values[0] / factor,
                        int(serviceToDoDict[activeInterface]['Band']) * values[1] / factor,
                        int(serviceToDoDict[activeInterface]['Band']) * values[2] / factor,
                        int(serviceToDoDict[activeInterface]['Band']) * values[3] / factor]
        serviceToDoDict[activeInterface]['scaledValues'] = scaledValues
        serviceToDoDict[activeInterface]['scale'] = scale
        newBand=int(serviceToDoDict[activeInterface]['Band'])/factor
        serviceToDoDict[activeInterface]['Band']=str(newBand)
        serviceToDoDict[activeInterface]['hostIP']=ip
    print(serviceToDoDict)

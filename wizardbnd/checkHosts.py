import database as db
import paramiko
import netmiko
from pandas import *
import re
import os
import SSHFunctions as sf
import threading
import xlparser as xlp
from pathlib import Path
import checkInput as ci
import sys


my_file = Path("/usr/local/nagiosxi/html/config/uploads/FILE.xlsx")


serverName=db.serverName  
community = db.serverList[serverName]['comm']

thread_list = []
pingResult = []
snmpResult = []
pingIpList = []
nopingIpList = []
snmpIpList=[]
nosnmpIpList=[]


class PingThread(threading.Thread):
    def __init__(self,hostIp,serverName):
        super(PingThread,self).__init__()

        self.hostIp=hostIp
        self.serverName=serverName

    def run(self):
        session = sf.connectSSH(self.serverName)
        command = "ping -c 1 " + self.hostIp
        result = session.send_command(command)
        #print(result)
        x = re.search("0 received", result)
        if (x):
            #pingResult[self.i] = {'ip':self.hostIp,'result':0}
            pingResult.append([self.hostIp, 0])
        else:
            #pingResult[self.i] = {'ip': self.hostIp, 'result':1}
            pingResult.append([self.hostIp, 1])



class SnmpThread(threading.Thread):
    def __init__(self,hostIp,serverName,community):
        super(SnmpThread,self).__init__()

        self.hostIp=hostIp
        self.serverName=serverName
        self.community = community

    def run(self):
        session = sf.connectSSH(self.serverName)
        command = 'snmpwalk -v 2c -c' + self.community + ' ' + self.hostIp + ' sysDescr'
        result = session.send_command(command)
        #print(result)
        x = re.search("\ATimeout: No Response", result)
        if (x):
            #snmpResult[self.i] = {'ip':self.hostIp,'result':'Not reachable through snmp'}
            snmpResult.append([self.hostIp, 0])
        else:
            #snmpResult[self.i] = {'ip': self.hostIp, 'result': 'Reachable through snmp'}
            snmpResult.append([self.hostIp, 1])




if my_file.is_file():
    xlsx = xlp.bulkHostCheckAsServices('/usr/local/nagiosxi/html/config/uploads/FILE.xlsx')

    for row in xlsx:
        try:
            hostIp = row['IP']
            threadPing = PingThread(hostIp, serverName)
            threadSnmp = SnmpThread(hostIp, serverName, community)
            thread_list.append(threadPing)
            thread_list.append(threadSnmp)
            threadPing.start()
            threadSnmp.start()
        except BaseException as e:
            logger.error(str(e))





    for thread in thread_list:
        thread.join()

    for [ip, result] in pingResult:
        if result:
            pingIpList.append(ip) # important output-feedback
        else:
            nopingIpList.append(ip) # important output-feedback

    for [ip, result] in snmpResult:
        if result:
            snmpIpList.append(ip) # important output-feedback
        else:
            nosnmpIpList.append(ip) # important output-feedback
else:
    ipsString = sys.argv[1]
    result=ci.checkIPs(ipsString)
    legalIps=result['legal'] # important output-feedback
    illegalIps=result['illegal'] # important output-feedback
    for ip in legalIps:
        try:
            hostIp=ip
            threadPing = PingThread(hostIp, serverName)
            threadSnmp = SnmpThread(hostIp, serverName, community)
            thread_list.append(threadPing)
            thread_list.append(threadSnmp)
            threadPing.start()
            threadSnmp.start()
        except BaseException as e:
            logger.error(str(e))
    for thread in thread_list:
        thread.join()

    for [ip, result] in pingResult:
        if result:
            pingIpList.append(ip) # important output-feedback
        else:
            nopingIpList.append(ip) # important output-feedback

    for [ip, result] in snmpResult:
        if result:
            snmpIpList.append(ip) # important output-feedback
        else:
            nosnmpIpList.append(ip) # important output-feedback


hosts = []
hosts1 = []
hosts2 = []
hosts3 = []
all=[]
for ip in pingIpList:
    if ip in snmpIpList:
        hosts.append(ip)
    elif ip in nosnmpIpList:
        hosts1.append(ip)
for ip in snmpIpList:
    if ip in nopingIpList:
        hosts2.append(ip)
for ip in nosnmpIpList:
    if ip in nopingIpList:
        hosts3.append(ip)
"""
print(hosts)
print(hosts1)
print(hosts2)
print(hosts3)"""

all.append(hosts)
all.append(hosts1)
all.append(hosts2)
all.append(hosts3)
print(all)
"""info = {}
info[0]={'ip':'176.16.10.96','serverName':'testnagios'}
info[1]={'ip':'176.16.10.229','serverName':'testnagios'}
snmpInfo = {}
snmpInfo[0]={'ip':'172.16.10.96','serverName':'testnagios','community':'routernagiosxi'}
snmpInfo[1]={'ip':'172.16.10.181','serverName':'testnagios','community':'switchnagiosxi'}




thread_list = []
for i in range(len(info)):
    try:

        hostIp = info[i]['ip']
        serverName = info[i]['serverName']
        thread = PingThread(i,hostIp,serverName)
        thread_list.append(thread)
        thread.start()
    except:
        print("Data not valid for input number {}".format(i))

for thread in thread_list:
    thread.join()


print("now")
print(pingResult)
thread_list = []
for i in range(len(snmpInfo)):
    try:

        hostIp = snmpInfo[i]['ip']
        serverName = snmpInfo[i]['serverName']
        community = snmpInfo[i]['community']
        thread = SnmpThread(i, hostIp, serverName, community)
        thread_list.append(thread)
        thread.start()
    except:
        print("Data not valid for input number {}".format(i))

for thread in thread_list:
    thread.join()


print("now")
print(snmpResult)
print(xlsx)
"""

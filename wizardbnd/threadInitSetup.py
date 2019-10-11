import SSHFunctions as sf
import RESTFunctions as rf
import threading



class setupHostsAndServices(threading.Thread):
    def __init__(self,totalDict,serverName,hostName,dictionary,hostDict):
        super(setupHostsAndServices,self).__init__()

        self.serverName=serverName
        self.dictionary = dictionary
        self.hostName = hostName
        self.hostDict = hostDict
        self.totalDict = totalDict

    def run(self):

        thread_list = []
        result = rf.createHost(self.serverName, self.hostName, self.hostDict[self.hostName]['ip'], self.hostDict[self.hostName]['contactgroup'],self.hostDict[self.hostName]['notes']).strip()
        rf.defineHostGroupsMembers(self.serverName,self.hostDict[self.hostName]['hostgroup'],self.hostName)
        pgresult = rf.createPingService(self.serverName, self.hostName).strip()
        seresult = rf.createCheckService(self.serverName, self.hostName, self.hostDict[self.hostName]['cpuwr'], self.hostDict[self.hostName]['cpucr'], self.hostDict[self.hostName]['memwr'] , self.hostDict[self.hostName]['memcr'] , self.hostDict[self.hostName]['tempwr'] , self.hostDict[self.hostName]['tempcr'] )


        self.totalDict['Hosts'][self.hostName] = {'HostResult': result,
                                        'PingResult': pgresult,
                                        'ServicesResults': seresult}


        serviceToDoDict, sysName = sf.getActiveIntefaceList(self.serverName, self.hostDict[self.hostName]['ip'])
        sf.touchRRD(self.serverName, self.hostDict[self.hostName]['ip'], serviceToDoDict)
        for activeInterface in serviceToDoDict.keys():
            thread = InterfaceService(serviceToDoDict,self.dictionary,self.hostDict, self.serverName, self.hostName, activeInterface,self.totalDict)
            thread_list.append(thread)
            thread.start()

        for thread in thread_list:
            thread.join()


class InterfaceService(threading.Thread):
    def __init__(self,serviceToDoDict,dictionary,hostDict, serverName, hostName, activeInterface,totalDict):
        super(InterfaceService,self).__init__()

        self.serviceToDoDict=serviceToDoDict
        self.activeInterface = activeInterface
        self.dictionary=dictionary
        self.hostName = hostName
        self.hostDict = hostDict
        self.serverName = serverName
        self.totalDict=totalDict

    def run(self):
        desc = self.serviceToDoDict[self.activeInterface]['Desc']
        alias = self.serviceToDoDict[self.activeInterface]['Alia']
        for i in range(0, len(self.dictionary)):
            if self.hostDict[self.hostName]['ip'] == self.dictionary[i]["help"] and self.activeInterface == self.dictionary[i]["portNo"]:
                scaledValues = [
                    self.dictionary[i]["inbww"], self.dictionary[i]["outbww"], self.dictionary[i]["inbwc"], self.dictionary[i]["outbwc"]
                ]
                scale = self.dictionary[i]["scale"]

        stresult = rf.createStatusService(self.serverName, self.hostName, desc, alias, self.activeInterface).strip()

        bwresult = rf.createBandwidthService(self.serverName, self.hostName, self.hostDict[self.hostName]['ip'], desc, alias,
                                             self.activeInterface, scaledValues, scale).strip()

        self.totalDict['Hosts'][self.hostName]['ServicesResults'][desc + ' ' + alias] = {'StatusResult': stresult,
                                                                               'BandwidthResult': bwresult}
import SSHFunctions as sf
import RESTFunctions as rf
import json
import threadInitSetup as tis



thread_list=[]


def setupHostsAndServices(serverName, hostiplist, hostgroup, contactgroup,cpuwr,cpucr,memwr,memcr,tempwr,tempcr,dictionary, hostnamelist=[], notes=[]):
    """ This function will automatically setup network hosts and services in a new Nagios server.

    :param serverName: Server ID
    :param hostiplist: List of host ips'. Critical component!!
    :param hostnamelist: List of host names. Only provide if you are sure of 1-to-1 correct hostname assignment. By
    default will assign the device's sysName as Nagios Host Name
    :param values: Values for Bandwidth services: [WarningDown, WarningUp, CriticalDown, CriticalUp]. Hardcoded to 0.75
    Warning UP/DOWN, 0.85 Critical UP/DOWN.
    :return: A dictionary of results.
    """
    totalDict = {}
    totalDict['Hosts'] = {}
    hostList = ''
    if hostnamelist != []:

        hostDict = {}
        if len(hostiplist) == len(hostnamelist):
            for i in range(0, len(hostiplist)):
                hostDict[hostnamelist[i]] = {'ip': hostiplist[i],'notes':notes[i], 'contactgroup':contactgroup[i],'hostgroup':hostgroup[i],'cpuwr':cpuwr[i],'cpucr':cpucr[i],'memwr':memwr[i],'memcr':memcr[i],'tempwr':tempwr[i],'tempcr':tempcr[i]}

        for hostName in hostDict.keys():
            thread = tis.setupHostsAndServices(totalDict,serverName,hostName,dictionary,hostDict)
            thread_list.append(thread)
            thread.start()

        for thread in thread_list:
            thread.join()


    sf.pushPlugin(serverName)
    coresult = rf.createCheckCustomCommand(serverName)

    totalDict['CheckCommand'] = coresult
    print(json.dumps(totalDict, indent=4))

    rf.applyConf(serverName)





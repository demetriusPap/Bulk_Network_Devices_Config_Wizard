import database as db
import requests as req
import json
import urllib3
import re
from pandas import *
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



def applyConf(serverName):
    ''' Applies configuration in Nagios XI

    :param serverName: Server ID.
    :return:
    '''
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/system/applyconfig?apikey=' + \
          db.serverList[serverName]['apikey']
    print(req.request('POST', url, verify=False).text)

def remove_html_tags(text):
    clean = re.compile('<.*>')
    return re.sub(clean, '', text)

def defineHostGroupsMembers(serverName,hostGroup,membersString=''):

    allmembersString=membersString+','+getHostGroupMembers('testnagios', hostGroup)

    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/hostgroup'+'?apikey=' + \
          db.serverList[serverName]['apikey']+'&pretty=1'
    body = {
        'hostgroup_name': hostGroup,
        'alias':'This host group has automatically created by wizzard',
        'members':allmembersString
    }
    response = req.request('POST', url, data=body, verify=False).text.strip()
    return response


def getHostGroupName(serverName):
    host_name_list = []
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/objects/hostgroup?apikey='+db.serverList[serverName]['apikey']+'&pretty=1'
    response = req.get(url, verify=False).text    
    jsonable = remove_html_tags(response)   
    
    response_json = json.loads(jsonable)
    
    host_list = response_json['hostgroup']
    try:
    	for dictionary in host_list:
        	host_name_list.append(dictionary["hostgroup_name"])
    except:
        
    	host_name_list=host_list['hostgroup_name']
    return host_name_list



def getHostGroupMembers(serverName,hostgroup):
    host_members_list = []
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/objects/hostgroupmembers?apikey='+db.serverList[serverName]['apikey']+'&pretty=1'
    response = req.get(url, verify=False).text
    jsonable = remove_html_tags(response)
    response_json = json.loads(jsonable)
    host_list = response_json['hostgroup']
    for dictionary in host_list:
        #hostgroup_list.append(dictionary["hostgroup_name"])
        if dictionary['hostgroup_name']==hostgroup:
            #print(dictionary)
            #host_members_list.append(dictionary["members"]['host'])
            """for dictionary2 in dictionary["members"]['host']:
                print(dictionary2)
                if isinstance(dictionary2, dict):
                    host_members_list.append(dictionary2['host_name'])
                else:
                    host_members_list.append(dictionary["members"]['host']['host_name'])"""
            if isinstance(dictionary['members']['host'],list):
                for dictionary2 in dictionary["members"]['host']:
                    host_members_list.append(dictionary2['host_name'])
            else:
                host_members_list.append(dictionary['members']['host']['host_name'])
    string = ",".join(map(str, host_members_list))
    return string


def getContactGroupMembers(serverName,contactgroup):
    contact_members_list = []
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/objects/contactgroupmembers?apikey='+db.serverList[serverName]['apikey']+'&pretty=1'
    response = req.get(url, verify=False).text
    jsonable = remove_html_tags(response)
    response_json = json.loads(jsonable)
    contact_list = response_json['contactgroup']
    for dictionary in contact_list:
        #hostgroup_list.append(dictionary["contactgroup_name"])
        if dictionary['contactgroup_name']==contactgroup:
            #print(dictionary)
            #contact_members_list.append(dictionary["members"]['host'])
            """for dictionary2 in dictionary["members"]['contact']:
                print(dictionary2)
                if isinstance(dictionary2, dict):
                    host_members_list.append(dictionary2['contact_name'])
                else:
                    host_members_list.append(dictionary["members"]['contact']['contact_name'])"""
            if isinstance(dictionary['members']['contact'],list):
                for dictionary2 in dictionary["members"]['contact']:
                    contact_members_list.append(dictionary2['contact_name'])
            else:
                contact_members_list.append(dictionary['members']['contact']['contact_name'])
    string = ",".join(map(str, contact_members_list))
    return string

def addHosttoHg(serverName,myhost,myhostgroup):
    members = getHostGroupMembers(serverName,myhostgroup) + ',' + myhost

    url = 'https://'+db.serverList[serverName]['ip']+'/nagiosxi/api/v1/config/hostgroup/'+myhostgroup+'?apikey=p7WPprSROEsS29NJhpiTlBKEgplcHX865kbN53VSWH2X7OWnduAB5BsFZ7QW5e2p&pretty=1&members='+members+'&applyconfig=1'
    request = req.request('PUT',url,verify=False).text
    return request

def addContacttoCg(serverName,mycontact,mycontactgroup):
    members = rf.getContactGroupMembers(serverName, mycontactgroup) + ',' + mycontact

    url = 'https://'+db.serverList[serverName]['ip']+'/nagiosxi/api/v1/config/contactgroup/'+mycontactgroup+'?apikey=p7WPprSROEsS29NJhpiTlBKEgplcHX865kbN53VSWH2X7OWnduAB5BsFZ7QW5e2p&pretty=1&members='+members+'&applyconfig=1'
    request = req.request('PUT',url,verify=False).text
    return request

def getContactGroupName(serverName):
    contact_name_list = []
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/objects/contactgroup?apikey='+db.serverList[serverName]['apikey']+'&pretty=1'
    response = req.get(url, verify=False).text
    jsonable = remove_html_tags(response)
    response_json = json.loads(jsonable)
    contact_list = response_json['contactgroup']
    try:
	    for dictionary in contact_list:
        	contact_name_list.append(dictionary["contactgroup_name"])
    except:
        
    	    contact_name_list=contact_list['contactgroup_name']
    return contact_name_list

def createHostGroup(hostGroupName,alias,serverName):
    body = {
        'hostgroup_name': hostGroupName,
        'alias': alias
    }

    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/hostgroup/testapihostgroup?apikey=' + \
          db.serverList[serverName]['apikey'] + '&applyconfig=1'

    request = req.request('POST',url,data=body,verify=False).text
    return request


def createContactGroup(contactgroupName,alias,serverName):
    body = {
        'contactgroup_name': contactgroupName,
        'alias': alias
    }

    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/contactgroup?apikey=' + \
          db.serverList[serverName]['apikey'] + '&applyconfig=1'

    request = req.request('POST',url,data=body,verify=False).text
    return request


def putServiceConfig(change, service, host, serverName):
    """ Applies a change to the configuration of a Service

    :param change: Change to be made
    :param service: Service to be modified
    :param host: Host of Service
    :param serverName: Server ID
    :return: Request text
    """
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service/' \
          + host + '/' + service + '?apikey=' + db.serverList[serverName]['apikey'] + change
    b = req.request('PUT', url + '&pretty=1&applyconfig=1', verify=False)

    return b.text.strip()


def createCheckService(serverName, hostName, cpuw,cpuc,memw,memc,tempw,tempc):
    """ Create the Service for the Check Cisco monitors

    :param serverName: Server ID
    :param hostList: List of hosts to be added to service
    :return: Dictionary of results
    """
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service?apikey=' + \
          db.serverList[serverName]['apikey']

    body = {
        'config_name': 'Check CPU',
        'host_name': hostName,
        'service_description': 'Check CPU',
        'check_command': 'check_cisco_custom\!' + db.serverList[serverName]['comm'] + '\!cpu\!-w '+cpuw+' -c '+cpuc,
        'check_interval': 5,
        'retry_interval': 1,
        'max_check_attempts': 5,
        'check_period': '24x7',
        'contacts': 'nagiosadmin',
        'notification_interval': 60,
        'notification_period': '24x7'
    }

    cpu = req.request('POST', url, data=body, verify=False).text.strip()

    body = {
        'config_name': 'Check MEM',
        'host_name': hostName,
        'service_description': 'Check MEM',
        'check_command': 'check_cisco_custom\!' + db.serverList[serverName]['comm'] + '\!mem\!-w '+memw+' -c '+memc,
        'check_interval': 5,
        'retry_interval': 1,
        'max_check_attempts': 5,
        'check_period': '24x7',
        'contacts': 'nagiosadmin',
        'notification_interval': 60,
        'notification_period': '24x7'
    }

    mem = req.request('POST', url, data=body, verify=False).text.strip()

    body = {
        'config_name': 'Check PSU',
        'host_name': hostName,
        'service_description': 'Check PSU',
        'check_command': 'check_cisco_custom\!' + db.serverList[serverName]['comm'] + '\!ps\!-w 1 -c 1',
        'check_interval': 5,
        'retry_interval': 1,
        'max_check_attempts': 5,
        'check_period': '24x7',
        'contacts': 'nagiosadmin',
        'notification_interval': 60,
        'notification_period': '24x7'
    }

    psu = req.request('POST', url, data=body, verify=False).text.strip()

    body = {
        'config_name': 'Check FAN',
        'host_name': hostName,
        'service_description': 'Check FAN',
        'check_command': 'check_cisco_custom\!' + db.serverList[serverName]['comm'] + '\!fan\!-w 1 -c 2',
        'check_interval': 5,
        'retry_interval': 1,
        'max_check_attempts': 5,
        'check_period': '24x7',
        'contacts': 'nagiosadmin',
        'notification_interval': 60,
        'notification_period': '24x7'
    }

    fan = req.request('POST', url, data=body, verify=False).text.strip()

    body = {
        'config_name': 'Check TEMP',
        'host_name': hostName,
        'service_description': 'Check TEMP',
        'check_command': 'check_cisco_custom\!' + db.serverList[serverName]['comm'] + '\!temp\!-w '+tempw+' -c '+tempc,
        'check_interval': 5,
        'retry_interval': 1,
        'max_check_attempts': 5,
        'check_period': '24x7',
        'contacts': 'nagiosadmin',
        'notification_interval': 60,
        'notification_period': '24x7'
    }

    temp = req.request('POST', url, data=body, verify=False).text.strip()

    return {'CPU': cpu,
            'MEM': mem,
            'PSU': psu,
            'TEMP': temp,
            'FAN': fan, }


def createPingService(serverName, hostName):
    """ Creates the Ping service for a host

    :param serverName: Server ID
    :param hostName: Host ID
    :return: Result
    """
    body = {
        'host_name': hostName,
        'service_description': 'Ping',
        'check_command': 'check_ping\!3000,80%\!5000,100%',
        'check_interval': 5,
        'retry_interval': 1,
        'max_check_attempts': 5,
        'check_period': '24x7',
        'contacts': 'nagiosadmin',
        'notification_interval': 60,
        'notification_period': '24x7'
    }

    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service?apikey=' + \
          db.serverList[serverName]['apikey']
    request = req.request('POST', url, data=body, verify=False).text
    return request


def createBandwidthService(serverName, hostName, hostip, intDesc, intAlias, activeInterface, values, scale):
    """ Creates the Bandwidth service for a particular Interface

    :param serverName: Server ID
    :param hostName: Host ID
    :param hostip: IP of host
    :param intDesc: Interface Description
    :param intAlias: Interface Alias
    :param activeInterface: Interface Index number
    :param values: Limit Values
    :param scale: Scale in mega,kilo or bytes
    :return: Result in text
    """
    if len(values) == 2:
        wd, wu, cd, cu = values[0], values[0], values[1], values[1]
    else:
        wd, wu, cd, cu = values[0], values[1], values[2], values[3]

    body = {
        'host_name': hostName,
        'service_description': intDesc + ' ' + intAlias + ' Bandwidth',
        'check_command': 'check_xi_service_mrtgtraf!' + hostip + '_' + activeInterface + '.rrd!' + str(wd) + ',' + str(
            wu)
                         + '!' + str(cd) + ',' + str(cu) + '!' + scale,
        'check_interval': 5,
        'retry_interval': 1,
        'max_check_attempts': 5,
        'check_period': '24x7',
        'contacts': 'nagiosadmin',
        'notification_interval': 60,
        'notification_period': '24x7'
        }

    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service?apikey=' + \
          db.serverList[serverName]['apikey']
    request = req.request('POST', url, data=body, verify=False).text
    return request


def createStatusService(serverName, hostName, intDesc, intAlias, activeInterface):
    """ Creates the Status service for a particular Interface

    :param serverName: Server ID
    :param hostName: Host ID
    :param intDesc: Interface Description
    :param intAlias: Interface Alias
    :param activeInterface: Interface Index number
    :return: Result in text
    """
    body = {
        'host_name': hostName,
        'service_description': intDesc + ' ' + intAlias + ' Status',
        'check_command': 'check_xi_service_ifoperstatus!' + db.serverList[serverName][
            'comm'] + '!' + activeInterface + '!-v 2 -p 161',
        'check_interval': 5,
        'retry_interval': 1,
        'max_check_attempts': 5,
        'check_period': '24x7',
        'contacts': 'nagiosadmin',
        'notification_interval': 6,
        'notification_period': '24x7'
    }
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service?apikey=' + \
          db.serverList[serverName]['apikey']
    request = req.request('POST', url, data=body, verify=False).text
    return request


def getServiceConfig(service, host, serverName):
    ''' Returns the configuration of a particular service.

    :param service: Service Description.
    :param host: Config Name.
    :param serverName: Server ID.
    :return: String.
    '''
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service?apikey=' + \
          db.serverList[serverName]['apikey'] + '&config_name=' + host \
          + '&service_description=' + service + '&pretty=1'
    return req.request('GET', url, verify=False).text


def getAllHostsList(serverName):
    ''' Returns the hosts in a server.

    :param serverName: Server ID.
    :return: List.
    '''
    print('Getting hosts')
    hostList = []
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/objects/hoststatus?apikey=' + \
          db.serverList[serverName]['apikey'] + '&pretty=1'
    for host in json.loads(req.request('GET', url, verify=False).text)['hoststatus']:
        hostList.append(host['name'])
    return sorted(hostList)


def getHostsbyService(serverName, service, toggle=True):
    ''' Returns the hosts registered into a service.

    :param serverName: Server ID.
    :param service: Service Description.
    :param toggle: True (Default) for included, False for Excluded hosts.
    :return: List.
    '''
    allHosts = getAllHostsList(serverName)
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service?apikey=' + \
          db.serverList[serverName]['apikey'] + '&pretty=1' + '&config_name=' + service

    checkHosts = json.loads(req.request('GET', url, verify=False).text)[0]['host_name']
    checkHostList = []
    for host in allHosts:
        if toggle == True:
            if host in checkHosts and host != 'localhost':
                checkHostList.append(host)
        else:
            if host not in checkHosts and host != 'localhost':
                checkHostList.append(host)
    return checkHostList


def getHostIP(serverName, hostName):
    ''' Returns the IP of a server.

    :param serverName: Server ID.
    :param hostName: Host Name
    :return: String.
    '''
    msg = 'Host not Found'
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/objects/host?apikey=' + \
          db.serverList[serverName]['apikey'] + '&pretty=1'
    for host in json.loads(req.request('GET', url, verify=False).text)['host']:
        if host['host_name'] == hostName:
            return host['address']
        else:
            continue
    return msg


def getAllServiceConfigs(serverName, hostList=[]):
    ''' Returns the config of every service on a list of hosts.

    :param serverName: Server ID.
    :param hostList: List of Host Names (Default empty list for every host).
    :return: Dict.
    '''
    serviceList = {}
    print('Getting services by host')
    if hostList == []:
        hostList = getAllHostsList(serverName)
    for host in hostList:
        url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service?apikey=' + \
              db.serverList[serverName]['apikey'] + '&pretty=1&config_name=' + host
        request = req.request('GET', url, verify=False).text
        services = json.loads(request)
        for config in services:
            try:
                if config['config_name'] in serviceList:
                    serviceList[config['config_name']].append(config['service_description'])
                else:
                    serviceList[config['config_name']] = [config['service_description']]
            except:
                continue
    return serviceList


def getServiceByKeyword(serverName, keywords=[[], []], hostlist=[]):
    ''' Returns dictionary of service configs, selected by keyword.

    :param serverName: Server ID.
    :param keywords: List of lists of Keywords (Default list of empty lists for every service).
    :param hostlist: List of Host Names (Default empty list for every host).
    :return: Dict
    '''
    keywordList = keywords[0]
    keywordNOTList = keywords[1]
    keyList = {}
    keyNotList = {}
    finalList = {}
    if hostlist == []:
        hostlist = getAllHostsList(serverName)
    servicelist = getAllServiceConfigs(serverName, hostlist)
    print('Managing keywords')
    try:
        for keyword in keywordList:
            keySubList = {}
            for host in servicelist.keys():
                for service in servicelist[host]:

                    if re.search(keyword, service):
                        if host in keySubList:
                            keySubList[host].append(service)
                        else:
                            keySubList[host] = [service]
            if keyword in keyList:
                keyList[keyword].append(keySubList)
            else:
                keyList[keyword] = [keySubList]
    except:
        pass
    try:
        for keyword in keywordNOTList:
            keySubList = {}
            for host in servicelist.keys():
                for service in servicelist[host]:

                    if re.search(keyword, service):
                        if host in keySubList:
                            keySubList[host].append(service)
                        else:
                            keySubList[host] = [service]

            if keyword in keyList:
                keyNotList[keyword].append(keySubList)
            else:
                keyNotList[keyword] = [keySubList]
    except:
        pass

    for host in hostlist:
        try:
            for service in servicelist[host]:
                correct = 0
                for key in keyList:
                    try:
                        if service in keyList[key][0][host]:
                            correct += 1
                        else:
                            correct = 0
                            break

                        for key in keyNotList:
                            if service not in keyNotList[key][0][host] and correct != 0:
                                continue
                            else:
                                correct = 0
                                break
                    except:
                        correct = 0
                if correct == len(keyList.values()):
                    if host in finalList:
                        finalList[host].append(service)
                    else:
                        finalList[host] = [service]
        except:
            continue

    print('Keyword-dependant service list collected')
    return finalList


def changeSelectedServices(server, keyword, values, change='bandlimits', hostlist=[]):
    ''' Makes a change to a list of services.

    :param server: Server ID.
    :param keyword: List of lists of Keywords.
    :param values: Values of changes to be implemented.
    :param change: Type of change to be implemented.
    :param hostlist: List of Host Names (Default empty list for every host).
    :return:
    '''
    servicelist = getServiceByKeyword(server, keyword, hostlist)
    if hostlist == []:
        hostlist = list(servicelist.keys())

    for host in hostlist:
        for service in servicelist[host]:

            runnConfig = getServiceConfig(service, host, server)
            a = re.search('^check_xi_service_mrtgtraf!(.+rrd)\!(.+)\!(.+)\!(.)',
                          json.loads(runnConfig)[0]['check_command'])
            if a.group(3) == '!':
                warn, crit, scale = re.search('(.+)!(.+)!(.)', a.group(2)).group(1), \
                                    re.search('(.+)!(.+)!(.)', a.group(2)).group(2), \
                                    re.search('(.+)!(.+)!(.)', a.group(2)).group(3)
            else:
                warn, crit, scale = a.group(2), a.group(3), a.group(4)

            b = re.search('(.+),(.+)', warn)
            c = re.search('(.+),(.+)', crit)

            if b == None:
                warnDown, warnUp = float(warn), float(warn)
            else:
                warnDown, warnUp = float(b.group(1)), float(b.group(2))

            if c == None:
                critDown, critUp = float(crit), float(crit)
            else:
                critDown, critUp = float(c.group(1)), float(c.group(2))

            if scale in ['K', 'k']:
                s = 1000
            elif scale in ['B', 'b']:
                s = 1000000
            else:
                s = 1
            if change == 'bandlimits':
                config = '&check_command=check_xi_service_mrtgtraf!' + a.group(1) + '!' + str(values[0] * s) + ',' \
                         + str(values[1] * s) + '!' + str(values[2] * s) + ',' + str(values[3] * s) + '!' + scale
                print(putServiceConfig(config, service, host, server))
                print(config)
                print(getServiceConfig(service, host, server))


def setMinimumLimits(server, keyword, values, hostlist=[]):
    ''' Sets minimum limit values.

    :param server: Server ID.
    :param keyword: List of lists of Keywords.
    :param values: Values of changes to be implemented.
    :param hostlist: List of Host Names (Default empty list for every host).
    :return:
    '''
    servicelist = getServiceByKeyword(server, keyword, hostlist)
    if hostlist == []:
        hostlist = list(servicelist.keys())
    resplist = []

    for host in hostlist:
        try:
            for service in servicelist[host]:

                runnConfig = getServiceConfig(service, host, server)
                a = re.search('^check_xi_service_mrtgtraf!(.+rrd)\!(.+)\!(.+)\!(.)',
                              json.loads(runnConfig)[0]['check_command'])
                if a.group(3) == '!':
                    warn, crit, scale = re.search('(.+)!(.+)!(.)', a.group(2)).group(1), \
                                        re.search('(.+)!(.+)!(.)', a.group(2)).group(2), \
                                        re.search('(.+)!(.+)!(.)', a.group(2)).group(3)
                else:
                    warn, crit, scale = a.group(2), a.group(3), a.group(4)

                b = re.search('(.+),(.+)', warn)
                c = re.search('(.+),(.+)', crit)

                if b == None:
                    warnDown, warnUp = float(warn), float(warn)
                else:
                    warnDown, warnUp = float(b.group(1)), float(b.group(2))

                if c == None:
                    critDown, critUp = float(crit), float(crit)
                else:
                    critDown, critUp = float(c.group(1)), float(c.group(2))

                if scale in ['K', 'k']:
                    s = 1000
                elif scale in ['B', 'b']:
                    s = 1000000
                else:
                    s = 1
                if (values[0] * s > warnDown) or (values[1] * s > warnUp) \
                        or (values[2] * s > critDown) or (values[3] * s > critUp):
                    config = '&check_command=check_xi_service_mrtgtraf!' + a.group(1) + '!' \
                             + str(values[0] * s) + ',' \
                             + str(values[1] * s) + '!' \
                             + str(values[2] * s) + ',' \
                             + str(values[3] * s) + '!' + scale
                    resp = putServiceConfig(config, service, host, server)
                    resplist.append(resp[7:-4])
        except:
            continue
    print(resplist)


def displaySelectedServices(server, keyword, hostlist=[]):
    ''' Displays, returns and exports a dictionary of services.

    :param server: Server ID.
    :param keyword: List of lists of Keywords.
    :param hostlist: List of Host Names (Default empty list for every host).
    :return: Dictionary
    '''
    resultdict = {}
    index = 0
    servicelist = getServiceByKeyword(server, keyword, hostlist)
    if hostlist == []:
        hostlist = list(servicelist.keys())
    print('Parsing results')
    for host in hostlist:
        for service in servicelist[host]:
            try:
                runnConfig = getServiceConfig(service, host, server)

                a = re.search('^check_xi_service_mrtgtraf!(.+rrd)\!(.+)\!(.+)\!(.)',
                              json.loads(runnConfig)[0]['check_command'])
                if a.group(3) == '!':
                    warn, crit, scale = re.search('(.+)!(.+)!(.)', a.group(2)).group(1), \
                                        re.search('(.+)!(.+)!(.)', a.group(2)).group(2), \
                                        re.search('(.+)!(.+)!(.)', a.group(2)).group(3)
                else:
                    warn, crit, scale = a.group(2), a.group(3), a.group(4)

                b = re.search('(.+),(.+)', warn)
                c = re.search('(.+),(.+)', crit)

                if b == None:
                    warnDown, warnUp = float(warn), float(warn)
                else:
                    warnDown, warnUp = float(b.group(1)), float(b.group(2))

                if c == None:
                    critDown, critUp = float(crit), float(crit)
                else:
                    critDown, critUp = float(c.group(1)), float(c.group(2))

                if scale in ['K', 'k']:
                    s = 1000
                elif scale in ['B', 'b']:
                    s = 1000000
                else:
                    s = 1
            except:
                continue
            index += 1
            resultdict[index] = {
                'Host': host,
                'Service': service,
                'WarningDown': warnDown,
                'WarningUp': warnUp,
                'CritDown': critDown,
                'CritUp': critUp,
                'Scale': scale,
                'MBScaledWarningDown': warnDown / s,
                'MBScaledWarningUp': warnUp / s,
                'MBScaledCritDown': critDown / s,
                'MBScaledCritUp': critUp / s}

    res = DataFrame.from_records(resultdict, index=['Host', 'Service', 'WarningDown', 'WarningUp', 'CritDown', 'CritUp',
                                                    'Scale', 'MBScaledWarningDown', 'MBScaledWarningUp',
                                                    'MBScaledCritDown', 'MBScaledCritUp']).T
    res.to_excel('Excel.xlsx')
    print('Results where also exported in a Results.xlsx file in the working directory.')
    return resultdict


def getServiceConfigbyFile(serverName, file):
    ''' Returns a dictionary of service configurations from a file of hosts and services.

    :param serverName: Server ID.
    :param file: Excel file of Hosts and Services.
    :return: Dictionary
    '''
    xls = ExcelFile(file)

    configList = {}
    df = xls.parse(xls.sheet_names[0]).to_dict()

    for count in range(1, len(df['Host'])):
        url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service?apikey=' \
              + db.serverList[serverName]['apikey'] + '&pretty=1&config_name=' \
              + df['Host'][count] + '&service_description=' + df['Service'][count]
        request = req.request('GET', url, verify=False).text
        services = json.loads(request)
        for config in services:
            try:
                if config['config_name'] in configList:
                    configList[config['config_name']].append(config['service_description'])
                else:
                    configList[config['config_name']] = [config['service_description']]
            except:
                continue
        return configList


def removeHostfromService(serverName, service, hostlist=[]):
    ''' Excludes a list of Hosts from a Service

    :param serverName: Server ID.
    :param hostlist: List of Host Names (Default empty list for every host).
    :param service: Config Name
    :return:
    '''
    if hostlist == []:
        hostlist = getAllHostsList(serverName)
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service?apikey=' + \
          db.serverList[serverName]['apikey'] + '&pretty=1&config_name=' + service
    request = req.request('GET', url, verify=False).text

    services = json.loads(request)
    for host in hostlist:
        if host in services[0]['host_name']:
            if len(services[0]['host_name']) == 1:
                services[0]['host_name'] = '*'
            else:
                services[0]['host_name'] = services[0]['host_name'].remove(host)
    print(services[0])
    print(service)
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service/' + services[0]['config_name'] \
          + '/' + services[0]['service_description'] + '?apikey=' + db.serverList[serverName]['apikey'] \
          + '&host_name=' + str(services[0]['host_name']) + '&pretty=1&applyconfig=1'
    print(req.request('PUT', url, verify=False).text)


def findManualServices(serverName):
    ''' Returns a dictionary of manually implemented services.

    :param serverName: Server ID.
    :return: Dictionary.
    '''
    manualServices = []
    hostlist = getAllHostsList(serverName)
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service?apikey=' \
          + db.serverList[serverName]['apikey'] + '&pretty=1'
    serviceConfigs = json.loads(req.request('GET', url, verify=False).text)
    for item in serviceConfigs:
        if item['config_name'] not in hostlist:
            manualServices.append(item['config_name'])
    return manualServices


def deleteHostServices(serverName, hostlist=[]):
    ''' Deletes the automatically implemented services of a host.

    :param serverName: Server ID.
    :param hostlist: List of Host Names (Default empty list for every host).
    :return:
    '''
    if hostlist == []:
        hostlist = getAllHostsList(serverName)
    for service in findManualServices(serverName):
        removeHostfromService(serverName, service, hostlist=hostlist)
    oblist = getAllServiceConfigs(serverName, hostlist)
    for host in oblist.keys():
        for service in oblist[host]:
            print(req.request('GET', 'http://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service' \
                                                                                   '?apikey='
                              + db.serverList[serverName]['apikey'] + '&pretty=1&config_name=' \
                              + host + '&service_description=' + service + '&pretty=1', verify=False).text)

            url = 'http://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service' \
                                                                '?apikey=' + db.serverList[serverName][
                      'apikey'] + '&pretty=1&host_name=' \
                  + host + '&service_description=' + service + '&applyconfig=1'
            servrequest = req.request('DELETE', url, verify=False).text
            print(servrequest)


def deleteHosts(serverName, hostlist=[]):
    ''' Deletes a list of hosts.

    :param serverName: Server ID.
    :param hostlist: List of Host Names (Default empty list for every host).
    :return:
    '''
    if hostlist == []:
        hostlist = getAllHostsList(serverName)
    deleteHostServices(serverName, hostlist)
    strhost = ''

    for host in hostlist:
        strhost = strhost + ('&host_name[]=' + host)
    url = 'http://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/host' \
                                                        '?apikey=' + db.serverList[serverName][
              'apikey'] + strhost + '&applyconfig=1'
    print(url)
    hostrequest = req.request('DELETE', url, verify=False).text
    print(hostrequest)


def createHost(serverName, hostName, ipAddr,contactgroup, notes='None,None'):
    ''' Creates a host.

    :param serverName: Server ID.
    :param hostName: Host Name.
    :param ipAddr: IP of host.
    :return:
    '''
    hostTemplate = {
        "host_name": hostName,
        "use": [
            "xiwizard_switch_host"
        ],
        "address": ipAddr,
        "parents": [
            ''
        ],
        "max_check_attempts": "5",
        "check_interval": "5",
        "retry_interval": "1",
        "check_period": "xi_timeperiod_24x7",
        "contacts": [
            "nagiosadmin"
        ],
        "contact_groups": [
            contactgroup
        ],
        "notification_interval": "60",
        "notification_period": "xi_timeperiod_24x7",
        "notes": notes,
        "icon_image": "switch.png",
        "statusmap_image": "switch.png",
        "_xiwizard": "switch",
        "register": "1"
    }

    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/host?apikey=' + \
          db.serverList[serverName]['apikey']
    request = req.request('POST', url, data=hostTemplate, verify=False).text
    return request




def addHosttoCheckService(serverName, hostlist=[]):
    ''' Adds a host to the list of Check services.

    :param serverName: Server ID.
    :param hostlist: List of Host Names (Default empty list for every host).
    :return:
    '''
    if hostlist == []:
        hostlist = getAllHostsList(serverName)
    servicelist = {}
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/command?apikey=' + \
          db.serverList[serverName]['apikey'] + '&pretty=1&command_name=Check_cisco_custom'
    if req.request('GET', url, verify=False).text[0:8] == "[\n    \n]":
        url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/command?apikey=' + \
              db.serverList[serverName]['apikey'] + '&pretty=1"'
        body = {'command_name': 'Check_cisco_custom',
                'command_line': '/usr/local/nagios/libexec/check_cisco.pl -H $HOSTADDRESS$ -C $ARG1$ -t $ARG2$ $ARG3$',
                'applyconfig': '1'}
    else:
        pass

    for name in ['Check Cpu', 'Check Mem', 'Check Temp', 'Check Fan', 'Check Psu']:
        changetoggle = 0
        url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service?apikey=' + \
              db.serverList[serverName]['apikey'] + '&pretty=1&config_name=' + name
        check = req.request('GET', url, verify=False).text

        if check[0:8] == "[\n    \n]":

            servicelist[name] = {'config_name': name,
                                 'host_name': hostlist,
                                 'service_description': name,
                                 'check_command': 'Check_cisco_custom!' + db.serverList[serverName]['comm'] +
                                                  db.checkcommand[name],
                                 'max_check_attempts': '5',
                                 'check_period': '24x7',
                                 'notification_period': '24x7',
                                 'register': '1',
                                 'check_interval': '5',
                                 'retry_interval': '5',
                                 'notification_interval': '5',
                                 'contacts': 'nagiosadmin',
                                 'applyconfig': '1'}

            url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service?apikey=' \
                  + db.serverList[serverName]['apikey'] + '&pretty=1&applyconfig=1'

            request = req.request('POST', url, data=servicelist[name], verify=False).text
            print(request)

        else:

            serviceHosts = json.loads(check)
            for host in hostlist:
                if host not in serviceHosts[0]['host_name']:
                    changetoggle = 1
                    serviceHosts[0]['host_name'].append(host)
            if changetoggle == 1:
                url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/service/' \
                      + serviceHosts[0]['config_name'] + '/' + serviceHosts[0]['service_description'] + '?apikey=' \
                      + db.serverList[serverName]['apikey'] + '&host_name=' \
                      + str(serviceHosts[0]['host_name'])[1:-1].replace(' ', '').replace("'", '') \
                      + '&pretty=1&applyconfig=1'

                request = req.request('PUT', url, verify=False).text
                print(request)


def findWarnings(serverName, hostlist=[]):
    if hostlist == []:
        hostlist = getAllHostsList(serverName)
    instancelist = {}
    for host in hostlist:

        url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/objects/statehistory?apikey=' \
              + db.serverList[serverName]['apikey'] + '&host_name=' + host + '&pretty=1'
        request = req.request('GET', url, verify=False).text
        services = []
        try:

            for change in json.loads(request)["stateentry"]:
                services.append(change['service_description'])
            instancelist[host] = {}

        except:
            continue
        uservices = []

        for item in services:
            if (item not in uservices) and (item != {}):
                uservices.append(item)
        for service in uservices:
            for item in json.loads(request)["stateentry"]:
                if item['service_description'] == service:
                    try:
                        instancelist[host][service] += 1
                    except:
                        instancelist[host][service] = 1
    newinstancelist = {}
    with open('temp.txt', 'w', newline='') as wr:
        wr.write('host|service|number of warnings\n')
        for host in instancelist.keys():
            for service in instancelist[host]:
                wr.write(host + '|' + service + '|' + str(instancelist[host][service]) + '\n')
                newinstancelist[host + ' / ' + service] = instancelist[host][service]

    print(json.dumps(newinstancelist, indent=4))

    df = read_csv('temp.txt', delimiter='|')
    with ExcelWriter('Out.xlsx') as writer:
        df.to_excel(writer, sheet_name='CorrectDataSheet', index=False)
    os.remove('temp.txt')


def createCheckCustomCommand(serverName):
    body = {
        'command_name': 'check_cisco_custom',
        'command_line': '/usr/local/nagios/libexec/check_cisco.pl -H $HOSTADDRESS$ -C $ARG1$ -t $ARG2$ $ARG3$'
    }
    url = 'https://' + db.serverList[serverName]['ip'] + '/nagiosxi/api/v1/config/command?apikey=' + \
          db.serverList[serverName]['apikey']
    request = req.request('POST', url, data=body, verify=False).text
    return request

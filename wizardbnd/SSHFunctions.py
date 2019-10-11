import database as db
import paramiko
import netmiko
from pandas import *
import re
import os


def connectSSH(serverName):
    ''' Connects to a server via SSH

    :param serverName: Server ID
    :return: Netmiko Session
    '''
    session = netmiko.ConnectHandler(device_type='cisco_ios',
                                     ip=db.serverList[serverName]['ip'],
                                     username=db.serverList[serverName]['userSSH'],
                                     password=db.serverList[serverName]['passSSH'])
    return session





def touchRRD(serverName, ip, activeintdict):
    """ Creates the .rrd files for a host's Bandwidth Service

    :param serverName: Server ID
    :param ip: IP of host
    :param activeintdict: Dictionary of active Interfaces
    :return:
    """
    ssh_sess = connectSSH(serverName)
    for interface in activeintdict.keys():
        command = 'touch /var/lib/mrtg/' + ip + '_' + interface + '.rrd'
        ssh_sess.send_command(command)


def getIDfromIP(serverName, ip):
    ''' Gets Identification from IP and checks against a list of known cisco devices.

    :param serverName: Server ID
    :param ip: IP of host
    :return: String
    '''
    ssh_sess = connectSSH(serverName)
    command = 'snmpwalk -v 2c -c' + db.serverList[serverName]['comm'] + ' ' + ip + ' sysObjectID'
    oid = '1.3.6.1.4.1' + ssh_sess.send_command(command)[56:]
    xls = ExcelFile('CiscoOIDexplanation.xlsx')
    df = xls.parse(xls.sheet_names[0]).to_dict()
    for count in range(0, len(df['OID'])):
        if df['OID'][count] == oid:
            return df['Model'][count]


def getActiveIntefaceList(serverName, ip):
    """ Polls a host for information.

    :param serverName: Server ID
    :param ip: IP of host to query.
    :return: Dictionary of values and sysName string
    """
    activePortList = []
    ignoredInt = []
    descDict = {}
    bandDict = {}
    aliaDict = {}
    compDict = {}
    ssh_sess = connectSSH(serverName)
    commandUp = 'snmpwalk -v 2c -c' + db.serverList[serverName]['comm'] + ' ' + ip + ' ifAdminStatus'
    interUpList = ssh_sess.send_command(commandUp)
    interUp = re.findall('ifAdminStatus\.(\d+) = INTEGER: [a-zA-Z]+\((\d)\)', interUpList)

    for portTuple in interUp:
        if portTuple[1] == '1':
            activePortList.append(portTuple[0])

    commandDesc = 'snmpwalk -v 2c -c' + db.serverList[serverName]['comm'] + ' ' + ip + ' ifDescr'
    interDescList = ssh_sess.send_command(commandDesc)
    interDesc = re.findall('ifDescr\.(\d+) = STRING: (\S+)', interDescList)

    for portTuple in interDesc:
        descDict[portTuple[0]] = portTuple[1]
        if re.search('[Nn]ull0', portTuple[1]) or re.search('StackSub', portTuple[1]):
            ignoredInt.append(portTuple[0])

    commandBand = 'snmpwalk -v 2c -c' + db.serverList[serverName]['comm'] + ' ' + ip + ' ifSpeed'
    interBandList = ssh_sess.send_command(commandBand)
    interBand = re.findall('ifSpeed\.(\d+) = Gauge32: (\S+)', interBandList)

    for portTuple in interBand:
        bandDict[portTuple[0]] = portTuple[1]



    commandAlia = 'snmpwalk -v 2c -c' + db.serverList[serverName]['comm'] + ' ' + ip + ' ifAlias'
    interAliaList = ssh_sess.send_command(commandAlia)
    interAlia = re.findall('ifAlias\.(\d+) = STRING: (.*)', interAliaList)

    for portTuple in interAlia:
        aliaDict[portTuple[0]] = " "




    commandName = 'snmpwalk -v 2c -c' + db.serverList[serverName]['comm'] + ' ' + ip + ' sysName'
    nameString = ssh_sess.send_command(commandName)
    hostName = re.search('= STRING: (.+)', nameString).group(1)
    for interface in activePortList:
        if interface not in ignoredInt:
            compDict[interface] = {
                'Desc': descDict[interface],
                'Band': bandDict[interface],
                'Alia': aliaDict[interface]
            }
        else:
            continue

    return compDict, hostName


def pushPlugin(serverName):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(db.serverList[serverName]['ip'],
                   username=db.serverList[serverName]['userSSH'],
                   password=db.serverList[serverName]['passSSH'])
    sftp = client.open_sftp()
    filename = os.path.realpath(__file__).replace('\\', '/')
    directory = os.path.dirname(filename).replace('\\', '/')
    sftp.put(directory + '/check_cisco.pl', '/usr/local/nagios/libexec/check_cisco.pl')
    sftp.close()
    ssh_sess = connectSSH(serverName)
    command = 'chmod +x /usr/local/nagios/libexec/check_cisco.pl'
    ssh_sess.send_command(command)

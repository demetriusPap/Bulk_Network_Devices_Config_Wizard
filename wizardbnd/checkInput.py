import re
import socket

ipregex = re.compile(
        #Valid IPs
        r"(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])")


def checkIPs(IpsString):
    hosts = IpsString.split(",")
    illegalips = []
    #print(tmp)
    for e in hosts:
        #print("e", e)
        if re.match(ipregex, e):
            #print("regular", e)
            pass
        else:
           # print("Irreggguuull",e)
            hosts.remove(e)
            illegalips.append(e)
            continue

        if e.isspace() or not e :
            hosts.remove(e)
            illegalips.append(e)
            continue


        if not re.match(ipregex, e):
            #print("regular",e)
            hosts.remove(e)
            illegalips.append(e)
            continue

        try:#if not valid ip it will throw exception
            socket.inet_aton(e)
            # legal
        except socket.error:
            hosts.remove(e)
            illegalips.append(e)
            continue
            #print("Found elegal IP", e)
    single=[]
    for unique in hosts:
        if unique not in single:
            single.append(unique)

    result = {
        "legal" : single,
        "illegal" : illegalips
    }

    return result

import re
import sys
import InitialSetup as ins
import database as db


correctScale=[]
notes = []
dictionary={}

host_inputs=sys.argv[1]
IP=sys.argv[2]
host_selector=sys.argv[3]
contact_selector=sys.argv[4]
lat_inputs=sys.argv[5]
long_inputs=sys.argv[6]
cpuwr=sys.argv[7]
cpucr=sys.argv[8]
memwr=sys.argv[9]
memcr=sys.argv[10]
tempwr=sys.argv[11]
tempcr=sys.argv[12]

inbww=sys.argv[13]
inbwc=sys.argv[14]
outbww=sys.argv[15]
outbwc=sys.argv[16]
scaleSelector=sys.argv[17]

help=sys.argv[18]
portNo=sys.argv[19]



host_inputs = re.search('host_inputs:(.*)', host_inputs)
IP = re.search('IP:(.*)', IP)
host_selector = re.search('host_selector:(.*)', host_selector)
contact_selector = re.search('contact_selector:(.*)', contact_selector)
lat_inputs = re.search('lat_inputs:(.*)', lat_inputs)
long_inputs = re.search('long_inputs:(.*)', long_inputs)
cpuwr = re.search('cpuwr:(.*)', cpuwr)
cpucr = re.search('cpucr:(.*)', cpucr)
memwr = re.search('memwr:(.*)', memwr)
memcr = re.search('memcr:(.*)', memcr)
tempwr = re.search('tempwr:(.*)', tempwr)
tempcr = re.search('tempcr:(.*)', tempcr)

inbww = re.search('inbww:(.*)', inbww)
inbwc = re.search('inbwc:(.*)', inbwc)
outbww = re.search('outbww:(.*)', outbww)
outbwc = re.search('outbwc:(.*)', outbwc)
scaleSelector = re.search('scaleSelector:(.*)', scaleSelector)

help = re.search('help:(.*)', help)
portNo = re.search('portNo:(.*)', portNo)




host_inputs = host_inputs[1].split(",")
IP= IP[1].split(",")
host_selector= host_selector[1].split(",")
contact_selector = contact_selector[1].split(",")
lat_inputs = lat_inputs[1].split(",")
long_inputs = long_inputs[1].split(",")
cpuwr= cpuwr[1].split(",")
cpucr = cpucr[1].split(",")
memwr = memwr[1].split(",")
memcr = memcr[1].split(",")
tempwr= tempwr[1].split(",")
tempcr = tempcr[1].split(",")

inbww = inbww[1].split(",")
inbwc = inbwc[1].split(",")
outbwc = outbwc[1].split(",")
outbww = outbww[1].split(",")
scaleSelector = scaleSelector[1].split(",")

help = help[1].split(",")
portNo = portNo[1].split(",")




for scale in scaleSelector:
    if scale =='Mbps':
        correctScale.append('M')
    elif scale=='Kbps':
        correctScale.append('K')
    else:
        correctScale.append('B')

for lat,long in zip(lat_inputs,long_inputs):
    notes.append('{},{}'.format(lat,long))

for i in range(0, len(help)):
    dictionary[i]={'portNo':portNo[i],'inbww':inbww[i],'inbwc':inbwc[i],'outbww':outbww[i],'outbwc':outbwc[i],'scale':correctScale[i],'help':help[i]}


ins.setupHostsAndServices(db.serverName,IP,host_selector,contact_selector,cpuwr,cpucr,memwr,memcr,tempwr,tempcr,dictionary,host_inputs,notes)


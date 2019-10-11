serverList = {}
mibList = {}


serverName='testnagios' #select the desired nagios server(nagios server name)



serverList['testnagios'] = {'apikey': 'p7WPprSROEsS29NJhpiT2BKEgplcHX865lbN53VSWH2X7OWnduAB5BsFZ7QW5e2p',
                            'ip': '181.59.11.169',
                            'userSSH': 'root',
                            'passSSH': 'mypsw',
                            'comm': 'mydevicescommunity'}

serverList['testnagios2'] = {'apikey': 'p7WPprSROEsS29NJhpiT222222cHX865lbN53VSWH2X7OWnduAB5BsFZ7QW5e2p',
                            'ip': '181.59.11.170',
                            'userSSH': 'root',
                            'passSSH': 'mypsw2',
                            'comm': 'mydevicescommunity2'}

serverList['testnagios3'] = {'apikey': 'p7WPprSROEsS29N333333HX865lbN53VSWH2X7OWnduAB5BsFZ7QW5e2p',
                            'ip': '181.59.11.171',
                            'userSSH': 'root',
                            'passSSH': 'mypsw3',
                            'comm': 'mydevicescommunity3'}

checkcommand = {
    'Check Cpu': '!cpu!-w 70 -c 80!!!!!',
    'Check Mem': '!mem!-w 15 -c 5!!!!!',
    'Check Temp': '!temp!-w 50 -c 80!!!!!',
    'Check Fan': '!fan!-w 1 -c 2!!!!!',
    'Check Psu': '!ps!-w 1 -c 1!!!!!'
}

mibList['EnterprisesPrefix'] = '1.3.6.1.4.1.'
mibList['C88X'] = {'hostname': mibList['EnterprisesPrefix'] + '9.2.1.3.0',
                   'temp status': mibList['EnterprisesPrefix'] + '9.9.13.1.3.1.6'}
mibList['ISR'] = {'hostname': mibList['EnterprisesPrefix'] + '9.9.23.1.3.4.0',
                  'sensors': mibList['EnterprisesPrefix'] + '9.9.91.1.1.1.1'}
mibList['C88X'] = {'hostname': '1.3.6.1.4.1.9.2.1.3.0',
                   'temp status': mibList['EnterprisesPrefix'] + '9.9.13.1.3.1.6'}


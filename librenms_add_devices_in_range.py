import requests

devices = []
for i in range (0,256):
    device = '10.100.20.' + str(i)
    devices.append(device)

devices2 = []
for i in range (0,256):
    device = '10.100.21.' + str(i)
    devices2.append(device)


api_token = 'KEY'

snmp_community = raw_input(str(('Input SNMP v2 Community: ')))

for switch in devices:
    #Add device to LibreNMS
    headers = {'X-Auth-Token': api_token,}
    data = '{"hostname":"' + switch + '","version":"v2c","community":"' + snmp_community + '"}'
    print(data)
    response = requests.post('http://10.32.26.51/api/v0/devices', headers=headers, data=data)
    print(response)


for switch in devices2:
    #Add device to LibreNMS
    headers = {'X-Auth-Token': api_token,}
    data = '{"hostname":"' + switch + '","version":"v2c","community":"' + snmp_community + '"}'
    print(data)
    response = requests.post('http://10.32.26.51/api/v0/devices', headers=headers, data=data)
    print(response)

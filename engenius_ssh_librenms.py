from __future__ import print_function,unicode_literals
import subprocess
import time
import getpass
import requests

engenious_devices = [
    '10.100.20.30',
    '10.100.20.31',
    '10.100.20.32',
    '10.100.20.33',
    '10.100.20.34',
    '10.100.20.35',
    '10.100.20.36',
    '10.100.20.37',
    '10.100.20.38',
    '10.100.20.39',
    '10.100.20.40',
    '10.100.20.41',
    '10.100.20.42',
    '10.100.20.43',
    '10.100.20.44',
    '10.100.20.45',
    '10.100.20.46',
    '10.100.20.47',
    '10.100.20.48',
    '10.100.20.49',
    '10.100.20.50',
    '10.100.20.51',
    '10.100.20.52',
    '10.100.20.53',
    '10.100.20.54',
    '10.100.20.55',
    '10.100.20.56',
    '10.100.20.57',
    ]

username = raw_input('Input Username: ')
password = (getpass.getpass())
api_token = 'API_KEY'
snmp_community = 'SNMP_STRING'

for device in engenious_devices:
    sshProcess = subprocess.Popen(['ssh',
        device],
        stdin=subprocess.PIPE,
        stdout = subprocess.PIPE,
        universal_newlines=True,
        bufsize=0)

    time.sleep(1)
    sshProcess.stdin.write(username + "\n")
    time.sleep(1)
    sshProcess.stdin.write(password + "\n")
    time.sleep(1)
    sshProcess.stdin.write("configure\n")
    time.sleep(1)
    sshProcess.stdin.write("sntp host 10.18.1.126\n")
    time.sleep(1)
    sshProcess.stdin.write("ip dns 10.18.1.19\n")
    time.sleep(1)
    sshProcess.stdin.write("no snmp community public\n")
    time.sleep(1)
    sshProcess.stdin.write("no snmp community private\n")
    time.sleep(1)
    sshProcess.stdin.write("no snmp community Stratacache\n")
    time.sleep(1)
    sshProcess.stdin.write("snmp community " + snmp_community + " ro\n")
    time.sleep(1)
    sshProcess.stdin.write("do save\n")
    time.sleep(2)
    sshProcess.stdin.write("exit\n")
    sshProcess.stdin.write("exit\n")
    sshProcess.stdin.close()

    for line in sshProcess.stdout:
        if line == "END\n":
            break
        print(line,end="")

    for line in sshProcess.stdout:
        if line == "END\n":
            break
        print(line,end="")

    headers = {
    'X-Auth-Token': api_token,}
    response = requests.delete('http://10.32.26.51/api/v0/devices/' + device + '', headers=headers)
    print('delete ' + device)
    print(response)

    headers = {'X-Auth-Token': api_token,}
    data = '{"hostname":"' + device + '","version":"v2c","community":"' + snmp_community + '"}'
    print(data)
    response = requests.post('http://10.32.26.51/api/v0/devices', headers=headers, data=data)
    print(response)


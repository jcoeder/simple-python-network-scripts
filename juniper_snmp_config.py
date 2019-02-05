import paramiko
import time
import getpass

juniper_devices = [
    '10.100.21.2',
    '10.100.21.3',
    '10.100.21.4',
    '10.100.21.5',
    '10.100.21.6',
    '10.100.21.7',
    '10.100.21.8',
    '10.100.21.9',
    '10.100.21.50',
    '10.100.21.51',
    '10.100.21.52',
    '10.100.21.53',
    ]

username = raw_input('Input Username: ')
password = (getpass.getpass())
snmp_community = raw_input(str(('Input SNMP v2 Community: ')))
snmp_location = raw_input(str(('Input SNMP Location: ')))
snmp_contact = raw_input(str(('Input Device Contact: ')))

for switch in juniper_devices:
    #Connect to switch and build ssh connection
    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(switch, username=username, password=password, look_for_keys=False, allow_agent=False)
    print('SSH connection established to ' + switch)
    remote_conn = remote_conn_pre.invoke_shell()
    print('Interactive SSH session established')

    #Print terminal to screen
    output = remote_conn.recv(1000)
    print(output)

    #Username root requires getting into the cli
    if username == 'root':
        remote_conn.send('cli\n')
        time.sleep(3)
        output = remote_conn.recv(1000)
        print(output)
    else:
        continue

    #Enter configuation mode
    remote_conn.send('configure\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

    #SNMP Configuration
    remote_conn.send('set snmp community ' + snmp_community + ' authorization read-only\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)
    remote_conn.send('set snmp location \"' + snmp_location + '\"' + '\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)
    remote_conn.send('set snmp contact \"' + snmp_contact + '\"' + '\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)
    remote_conn.send('set snmp routing-instance-access\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

    #Save configuration
    remote_conn.send("commit\n")
    time.sleep(4)
    output = remote_conn.recv(1000)
    print(output)

    #Exit configuation mode
    remote_conn.send('exit\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

    remote_conn.send('exit\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

    remote_conn.send('exit\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

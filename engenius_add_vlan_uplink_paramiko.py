import paramiko
import time
import getpass

'''
A list of lists.  First item in the nested list should be
the switches IP address or hostname and the second item
should be the switch's uplink interface.
'''
engenius = [
    ['172.31.33.180', 'interface gigabitethernet 49'],
    ['172.31.33.181', 'interface gigabitethernet 49'],
    ['172.31.33.182', 'interface gigabitethernet 49'],
    ['172.31.33.183', 'interface gigabitethernet 49'],
    ]

username = raw_input('Input Username: ')
password = (getpass.getpass())
print('Input VLAN ID to be added: ')
vlan_id = str(input())
vlan_name = raw_input('Input VLAN name: ')

for switch in engenius:
    #Connect to switch and build ssh connection
    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(switch, username=username, password=password, look_for_keys=False, allow_agent=False)
    print('SSH connection established to ' + switch[0])
    remote_conn = remote_conn_pre.invoke_shell()
    print('Interactive SSH session established')

    #Print terminal to screen
    output = remote_conn.recv(1000)
    print(output)

    #Enter configuation mode
    remote_conn.send('configure\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

    #Add VLAN
    print('Creating VLAN')
    remote_conn.send('vlan ' + vlan_id + '\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)
    remote_conn.send('name ' + vlan_name + '\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)
    remote_conn.send('exit\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

    #Enter configuation mode
    remote_conn.send('configure\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

    #Add VLAN to uplink
    print('Adding VLAN to uplink')
    remote_conn.send(switch[1] + '\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    remote_conn.send('switchport hybrid allowed vlan add ' + vlan_id + ' tagged\n')
    time.sleep(1)
    output = remote_conn.recv(1000)

    #Exit configuation mode
    remote_conn.send('exit\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

    #Save configuration
    remote_conn.send("save\n")
    time.sleep(2)
    output = remote_conn.recv(1000)
    print(output)

import paramiko
import time
import getpass

juniper_ex4300 = ['10.100.20.11', '10.100.20.22', '10.100.20.23', '10.100.20.25']

username = raw_input('Input Username: ')
password = (getpass.getpass())
print('Input VLAN ID to be added: ')
vlan_id = str(input())
vlan_name = raw_input('Input VLAN name: ')

for switch in juniper_ex4300:
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

    #Enter configuation mode
    remote_conn.send('configure\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

    #Add VLAN
    remote_conn.send('set vlans VLAN' + vlan_id + ' description ' + vlan_name + '\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

    #Exit configuation mode
    remote_conn.send('exit\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

    #Save configuration
    remote_conn.send("commit\n")
    time.sleep(4)
    output = remote_conn.recv(1000)
    print(output)

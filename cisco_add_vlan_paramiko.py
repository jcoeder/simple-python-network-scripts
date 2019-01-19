import paramiko
import time
import getpass

cisco_cat = ['172.31.33.180', '10.100.20.22', '10.100.20.23', '10.100.20.25']

username = raw_input('Input Username: ')
password = (getpass.getpass())
print('Input Enable Password - For none, press enter: ')
enable_password = (getpass.getpass())
print('Input VLAN ID to be added: ')
vlan_id = str(input())
vlan_name = raw_input('Input VLAN name: ')

for switch in cisco_cat:
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

    #If enable is required
    if '>' in output:
        remote_conn.send('enable\n')
        time.sleep(1)
        output = remote_conn.recv(1000)
        print(output)
        if 'Password:' in output:
            remote_conn.send(enable_password + '\n')
            time.sleep(1)
            output = remote_conn.recv(1000)
            print(output)
        else:
            pass
    else:
        pass

    #Enter configuation mode
    remote_conn.send('configure terminal\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

    #Add VLAN
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

    #Exit configuation mode
    remote_conn.send('exit\n')
    time.sleep(1)
    output = remote_conn.recv(1000)
    print(output)

    #Save configuration
    remote_conn.send("write\n")
    time.sleep(2)
    output = remote_conn.recv(1000)
    print(output)

import requests
import ipaddress

url = 'https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt'
url = 'https://www.team-cymru.org/Services/Bogons/fullbogons-ipv6.txt'

response = requests.get(url)
list_response = response.text.split('\n')
print(list_response)


ipaddress.IPv4Network('192.168.0.0/24').netmask
ipaddress.IPv4Network('192.168.0.0/24').with_netmask

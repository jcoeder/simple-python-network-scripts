"""
Script to compare a 1-to-1 interfaces mapping for Cisco switches
Looks for access and voice vlan configurations and compares them
between the new and the old interface.
"""

__author__ = "Justin Oeder"
__version__ = "0.0.1"
__license__ = "MIT"

from ciscoconfparse import CiscoConfParse


old_conf = CiscoConfParse('Old Config.txt', syntax='ios')
new_conf = CiscoConfParse('New Config.txt', syntax='ios')


old_interfaces = {}
new_interfaces = {}
	
	
for intf_obj in old_conf.find_objects('^interface'):
    intf_name = intf_obj.re_match_typed('^interface\s+(\S.+?)$')
    intf_access_vlan = intf_obj.re_match_iter_typed(r'switchport\saccess\svlan\s\d+', result_type=str, group=0, default ='NOT AN ACCESS PORT')
    intf_voice_vlan = intf_obj.re_match_iter_typed(r'switchport\svoice\svlan\s\d+', result_type=str, group=0, default ='NOT CONFIGURED FOR VOICE VLAN')
    old_interfaces[intf_name] = {}
    old_interfaces[intf_name]['access_vlan'] = intf_access_vlan
    old_interfaces[intf_name]['voice_vlan'] = intf_voice_vlan
	
	
for intf_obj in new_conf.find_objects('^interface'):
    intf_name = intf_obj.re_match_typed('^interface\s+(\S.+?)$')
    intf_access_vlan = intf_obj.re_match_iter_typed(r'switchport\saccess\svlan\s\d+', result_type=str, group=0, default ='NOT AN ACCESS PORT')
    intf_voice_vlan = intf_obj.re_match_iter_typed(r'switchport\svoice\svlan\s\d+', result_type=str, group=0, default ='NOT CONFIGURED FOR VOICE VLAN')
    new_interfaces[intf_name] = {}
    new_interfaces[intf_name]['access_vlan'] = intf_access_vlan
    new_interfaces[intf_name]['voice_vlan'] = intf_voice_vlan
	
	
common_interfaces = {}
uncommon_interfaces = {}


for key in old_interfaces:
    if not(key in new_interfaces and old_interfaces[key] == new_interfaces[key]):
	    uncommon_interfaces[key] = old_interfaces[key]
    elif (key in new_interfaces and old_interfaces[key] == new_interfaces[key]) and (new_interfaces[key]['access_vlan'] == old_interfaces[key]['access_vlan']) and (new_interfaces[key]['voice_vlan'] == old_interfaces[key]['voice_vlan']):
        common_interfaces[key] = old_interfaces[key]
    elif (key in new_interfaces and old_interfaces[key] == new_interfaces[key]) and (new_interfaces[key]['access_vlan'] != old_interfaces[key]['access_vlan']) or (new_interfaces[key]['voice_vlan'] != old_interfaces[key]['voice_vlan']):
        uncommon_interfaces[key] = old_interfaces[key]


for key in new_interfaces:
    if not(key in old_interfaces and new_interfaces[key] == old_interfaces[key]):
	    uncommon_interfaces[key] = new_interfaces[key]


with open('results.txt', 'w') as f:
    for key in common_interfaces:
        print(key)
        f.write(key + '\n')

        print("New Configuration")
        f.write("New Configuration\n")

        try:
            print(new_interfaces[key])
            f.write(str(new_interfaces[key]) + '\n')
        except KeyError:
            print('Interface does not exist')
            f.write('Interface does not exist\n')

        print("Old Configuration")
        f.write("Old Configuration\n")

        try:
            print(old_interfaces[key])
            f.write(str(old_interfaces[key]) + '\n')
        except KeyError:
            print('Interface does not exist')
            f.write('Interface does not exist\n')
        print('')
        f.write('\n')
		
    for key in uncommon_interfaces:
        print(key)
        f.write(key + '\n')

        print("New Configuration")
        f.write("New Configuration\n")

        try:
            print(new_interfaces[key])
            f.write(str(new_interfaces[key]) + '\n')
        except KeyError:
            print('Interface does not exist')
            f.write('Interface does not exist\n')

        print("Old Configuration")
        f.write("Old Configuration\n")

        try:
            print(old_interfaces[key])
            f.write(str(old_interfaces[key]) + '\n')
        except KeyError:
            print('Interface does not exist')
            f.write('Interface does not exist\n')
        print('')
        f.write('\n')

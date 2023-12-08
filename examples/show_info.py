import sys
import time
sys.path.insert(0, sys.path[0]+"/../")
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient()

action_dict = dict()
action_dict[1] = 'Profile List'
action_dict[2] = 'Group List'
action_dict[3] = 'Traffic Package List'
action_dict[4] = 'Proxy List'

print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Please enter a number to select a list to view:')
for k in action_dict:
    print('  ', k, action_dict[k])

print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'You can also enter \'x\' or \'X\' to exit.')
while True:
    action_index = input("Please enter the number:")
    if action_index == 'x' or action_index == 'X':
        break

    action_index = int(action_index)
    if action_index not in action_dict:
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'List does not exist')
    elif action_index == 1:
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), action_index, '=', action_dict[action_index])
        data = c.get_profile_list()
        if data is None:
            print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Get profile list error:')
            print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
            print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
            sys.exit()
        else:
            for item in data:
                print('  ', item['profile_id'], item['name'], item['site_url'])
    elif action_index == 2:
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), action_index, '=', action_dict[action_index])
        data = c.get_group_list()
        if data is None:
            print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Get group list error:')
            print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
            print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
            sys.exit()
        else:
            for item in data:
                print('  ', item['id'], item['title'])
    elif action_index == 3:
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), action_index, '=', action_dict[action_index])
        data = c.get_traffic_package_list()
        if data is None:
            print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Get traffic package list error:')
            print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
            print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
            sys.exit()
        else:
            for item in data:
                print('  ', item['id'], item['limit_flow'], item['used_flow'], item['supply_name'])
    elif action_index == 4:
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), action_index, '=', action_dict[action_index])
        data = c.get_proxy_list()
        if data is None:
            print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Get proxy list error:')
            print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
            print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
            sys.exit()
        else:
            for item in data:
                print('  ', item['id'], item['proxy_type'], item['proxy_ip'], item['proxy_port'], item['proxy_user'], item['proxy_password'])

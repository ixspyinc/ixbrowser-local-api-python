import sys
import time
sys.path.insert(0, sys.path[0]+"/../")
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient()

"""
# clear profile cache by profile id list
profile_id = [250, 251]
data = c.clear_profile_cache(profile_id)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""

"""
# update profile to purchased proxy mode
proxy_id = 29040
profile_id = 250
data = c.update_profile_to_purchased_proxy_mode(profile_id, proxy_id)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""

"""
# update profile to custom proxy mode
profile_id = 250
proxy_type = 'direct'
# proxy_type = 'socks5'
# proxy_ip = '192.168.7.96'
# proxy_port = '20001'

data = c.update_profile_to_custom_proxy_mode(profile_id, proxy_type)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""

"""
# random profile fingerprint
profile_id = 250
data = c.random_profile_fingerprint(profile_id)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""

"""
# get profile cookies
profile_id = 251
data = c.get_profile_cookies(profile_id)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""

"""
# update profile cookies
profile_id = 250
cookie = None
data = c.update_profile_cookie(profile_id, cookie)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""

"""
# delete profile
profile_id = 250
cookie = None
data = c.delete_profile(profile_id)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""
"""
# empty recycle in
data = c.empty_recycle_bin()
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
    print('recycle bin has been emptied.')
"""

"""
# close profile in batches
profile_id = [254, 251]

for p_id in profile_id:
    open_result = c.open_profile(p_id, cookies_backup=False, load_profile_info_page=False)
    if open_result is None:
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Open profile error:')
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    else:
        print(p_id, open_result)

time.sleep(30)

data = c.close_profile_in_batches(profile_id)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(profile_id, 'result:', data)
"""

"""
# update profile to traffic package mode
profile_id = 250
proxy_id = 10
country = 'us'
city = 'Ada'
traffic_package_gateway = 'US-US'

data = c.update_profile_to_traffic_package_mode(profile_id, proxy_id, country, city, traffic_package_gateway)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""

"""
# update profile groups in_batches
profile_id = [250, 251]
proxy_id = 77
data = c.update_profile_groups_in_batches(profile_id, proxy_id)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""
"""
# create group
name = 'test'
sort = 1000
data = c.create_group(name, sort)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""

"""
# update group
group_id = 7392
name = 'test1'
data = c.update_group(group_id, name, sort=999)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""

"""
# delete group
group_id = 7392
data = c.delete_group(group_id)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""

"""
# create custom proxy
proxy_type = 'socks5'
proxy_ip = '192.168.7.92'
proxy_port = '20001'
proxy_user = 'test'
proxy_password = 'test'
note = 'teset'
data = c.create_proxy(proxy_type, proxy_ip, proxy_port, proxy_user, proxy_password, note)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""

"""
# update custom proxy
proxy_id = 757041
proxy_type = 'http'
proxy_ip = '192.168.7.93'
proxy_port = '20002'
proxy_user = 'test1'
proxy_password = 'test1'
note = 'teset1'
data = c.create_proxy(proxy_type, proxy_ip, proxy_port, proxy_user, proxy_password, note)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""

"""
# delete proxy
proxy_id = 757071
data = c.delete_proxy(proxy_id)
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
else:
    print(data)
"""
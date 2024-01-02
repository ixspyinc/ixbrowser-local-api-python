import sys
import time
sys.path.insert(0, sys.path[0]+"/../")
from ixbrowser_local_api import IXBrowserClient
from ixbrowser_local_api import Profile, Proxy, Preference, Fingerprint, Consts


c = IXBrowserClient()
c.show_request_log = True

# Object properties are set one by one
p = Profile()
p.random_color()
p.site_url = 'https://www.ixbrowser.com'
p.name = 'Temp ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
p.tag = ['test', 'test1']

proxy = Proxy()

# custom proxy
proxy.change_to_custom_mode(Consts.PROXY_TYPE_SOCKS5, '127.0.0.1', '10808')

# purchased proxy
# proxy.change_to_purchased_mode(1)

# traffic package proxy
# proxy.change_to_traffic_package_mode(1, 'us', ip_policy=True, ip_detection=True)

# extract from url
'''
json_mapping = proxy.get_url_extraction_mode_json_mapping("ip", "port")
proxy.change_to_url_extraction_mode('https://127.0.0.1/extract_url', 
                                    format_type=Consts.PROXY_DATA_FROMAT_TYPE_JSON,
                                    json_mapping=json_mapping
                                    )
'''

bypass_ls = ['*.ipinfo.io', 'ixbrowser.com']
proxy.set_bypass_list(bypass_ls)

p.proxy_config = proxy

preference = Preference()
preference.set_cloud_backup(1, 1, 0)
preference.block_audio = 1
preference.block_image = 1
preference.open_url = 'https://www.google.com'
preference.load_profile_info_page = 0
p.preference_config = preference

fingerprint = Fingerprint()
fingerprint.language_type = 2
fingerprint.language = 'cn'
fingerprint.client_rects = 0
fingerprint.set_device_name('rand_' + str(int(time.time())))
p.fingerprint_config = fingerprint



"""
# Assign values to object properties in batches through dictionaries
p_dict = dict()
p_dict['color'] = '#ff0000'
p_dict['site_url'] = 'https://www.ixbrowser.com'
p_dict['name'] = 'Temp ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

p_dict['proxy_config'] = dict()
p_dict['proxy_config']['proxy_mode'] = 2
p_dict['proxy_config']['proxy_type'] = 'socks5'
p_dict['proxy_config']['proxy_ip'] = '127.0.0.1'
p_dict['proxy_config']['proxy_port'] = '10808'

p_dict['preference_config'] = dict()
p_dict['preference_config']['block_audio'] = 1
p_dict['preference_config']['block_image'] = 1
p_dict['preference_config']['cookies_backup'] = 0
p_dict['preference_config']['open_url'] = 'https://www.google.com'

p_dict['fingerprint_config'] = dict()
p_dict['fingerprint_config']['language_type'] = 2
p_dict['fingerprint_config']['language'] = 'cn'
p_dict['fingerprint_config']['client_rects'] = 0

p = Profile(p_dict)
"""

result = c.create_profile(p)
if result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Create Profile error:')
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
else:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'result:', result)


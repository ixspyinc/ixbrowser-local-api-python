import sys
import time
from ixbrowser_local_api import IXBrowserClient
from ixbrowser_local_api import Profile, Proxy, Preference, Fingerprint


c = IXBrowserClient()

# Object properties are set one by one
p = Profile()
p.random_color()
p.site_url = 'https://www.ixbrowser.com'
p.name = 'Temp ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
proxy = Proxy()
proxy.proxy_mode = 2
proxy.proxy_type = 'socks5'
proxy.proxy_ip = '192.168.7.96'
proxy.proxy_port = '20001'
p.proxy_config = proxy

preference = Preference()
preference.block_audio = 1
preference.block_image = 1
preference.cookies_backup = 0
preference.open_url = 'https://www.google.com'
p.preference_config = preference

fingerprint = Fingerprint()
fingerprint.language_type = 2
fingerprint.language = 'cn'
fingerprint.client_rects = 0
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
p_dict['proxy_config']['proxy_ip'] = '192.168.7.96'
p_dict['proxy_config']['proxy_port'] = '20001'

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


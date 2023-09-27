import sys
import time
from ixbrowser_local_api import IXBrowserClient
from ixbrowser_local_api import Profile, Proxy, Preference, Fingerprint, Consts


c = IXBrowserClient()
c.show_request_log = True

p = Profile()
p.profile_id = 249
p.random_color()
p.site_url = 'https://www.ixbrowser.com'
p.name = 'Temp ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

fp = Fingerprint()
fp.ua_info = 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5735.138 Safari/537.36'
p.fingerprint_config = fp

preference = Preference()
preference.open_url = 'https://www.google.com'

preference.block_image = 1
p.preference_config = preference

proxy = Proxy()
proxy.change_to_custom_mode(Consts.PROXY_TYPE_SOCKS5, '127.0.0.1', '10808')
p.proxy_config = proxy

result = c.update_profile(p)
if result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Update profile error:')
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
else:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'result:', result)


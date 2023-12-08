import sys
import time
sys.path.insert(0, sys.path[0]+"/../../")
from ixbrowser_local_api import IXBrowserClient
from ixbrowser_local_api import Proxy, Consts

c = IXBrowserClient()
c.show_request_log = True

transfer_code = '12345678-12345678'
p = Proxy()
p.change_to_custom_mode(Consts.PROXY_TYPE_SOCKS5, '127.0.0.1', '10808')
bypass_ls = ['*.gvt1.com', 'update.googleapis.com', 'www.gstatic.com']
p.set_bypass_list(bypass_ls)


result = c.import_profile_via_transfer_code(transfer_code, p)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Import Profile via Transfer Code:')
if result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
else:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Result:', result)


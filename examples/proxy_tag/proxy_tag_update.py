import logging

import sys
import time
sys.path.insert(0, sys.path[0]+"/../../")
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient()
logging.basicConfig(level=logging.WARNING)
logging.getLogger('ixbrowser_local_api').setLevel(logging.DEBUG)

# 
id = 192
name = 'test_' + str(int(time.time()))

result = c.update_proxy_tag(id, name)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Update Proxy Tag')
if result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
else:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Result:', result)


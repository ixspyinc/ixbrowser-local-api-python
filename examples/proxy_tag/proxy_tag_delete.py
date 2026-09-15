import logging

import sys
import time
sys.path.insert(0, sys.path[0]+"/../../")
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient()
logging.basicConfig(level=logging.WARNING)
logging.getLogger('ixbrowser_local_api').setLevel(logging.DEBUG)


id = 192

result = c.delete_proxy_tag(id)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Delete Proxy Tag')
if result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
else:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Result:', result)


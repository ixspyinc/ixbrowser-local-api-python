import sys
import time
sys.path.insert(0, sys.path[0]+"/../../")
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient()
c.show_request_log = True

name = 'test'


result = c.create_tag(name)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Create Tag')
if result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
else:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Result:', result)


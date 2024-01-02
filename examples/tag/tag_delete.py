import sys
import time
sys.path.insert(0, sys.path[0]+"/../../")
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient()
c.show_request_log = True


tag_id = 289

result = c.delete_tag(tag_id)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Delete Tag')
if result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
else:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Result:', result)


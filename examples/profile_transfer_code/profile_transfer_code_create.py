import sys
import time
sys.path.insert(0, sys.path[0]+"/../../")
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient()
c.show_request_log = True

profile_id = 1
# login password
login_pwd = 'xxxxxxxx'


result = c.create_profile_transfer_code(profile_id, login_pwd, 1, 1, 1)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Create Profile Transfer Code:')
if result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
else:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Result:', result)


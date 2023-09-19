import sys
import time
from ixbrowser_local_api import IXBrowserClient
from ixbrowser_local_api import Profile


c = IXBrowserClient()

p = Profile()
p.profile_id = 250
# p.random_color()
p.site_url = 'https://www.ixbrowser.com'
p.name = 'Temp ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

result = c.update_profile(p)
if result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Update profile error:')
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
else:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'result:', result)


import sys
import time
sys.path.insert(0, sys.path[0]+"/../")
from ixbrowser_local_api import IXBrowserClient
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

"""
Get the profile list, open the latest profile, then visit the ixbrowser homepage, and close it after the last 30 seconds.

Required installation
pip install ixbrowser-local-api
pip install selenium

More information
https://github.com/ixspyinc/ixbrowser-local-api-python
"""

c = IXBrowserClient()
data = c.get_profile_list()
if data is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Get profile list error:')
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()

if len(data) == 0:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Please create a profile first.')
    sys.exit()

item = data[0]

profile_id = item['profile_id']

print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'profile_id=', profile_id)

open_result = c.open_profile(profile_id, cookies_backup=False, load_profile_info_page=False)
if open_result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Open profile error:')
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
# time.sleep(30)
web_driver_path = open_result['webdriver']
debugging_address = open_result['debugging_address']

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debugging_address)

# selenium 3 version
# driver = Chrome(web_driver_path, chrome_options=chrome_options)

# selenium 4 and above
driver = Chrome(service=Service(web_driver_path), options=chrome_options)

print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Visit the ixBrowser homepage by default')
driver.get("https://www.ixbrowser.com")
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Automatically exit after 30 seconds')
time.sleep(30)

"""
# close_profile is currently a forced process kill method, which will cause browser exceptions.
close_result = c.close_profile(profile_id)
if close_result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Close profile error:')
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
"""

# Improve the close method so that there will be no abnormal shutdown prompt on subsequent startups.
c.close_profile(profile_id)


print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'window closed.')

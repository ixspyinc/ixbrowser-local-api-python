import sys
import time
from ixbrowser_local_api import IXBrowserClient
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

"""
Get the Profile list, open the latest profile, then visit the ixbrowser homepage, and close it after the last 30 seconds.

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

web_driver_path = open_result['webdriver']
debugging_address = open_result['debugging_address']

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debugging_address)
driver = Chrome(web_driver_path, chrome_options=chrome_options)

print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Visit the ixBrowser homepage by default')
driver.get("https://www.ixbrowser.com")
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Automatically exit after 30 seconds')
time.sleep(30)

# close_profile is currently a forced process kill method, which will cause browser exceptions.
# It is recommended to use selenium to close the window.
"""
close_result = c.close_profile(profile_id)
if close_result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Close profile error:')
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
"""

c.close_profile_via_selenium(driver)

print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'window closed.')

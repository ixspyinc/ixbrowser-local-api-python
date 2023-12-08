import sys
import time
import random
sys.path.insert(0, sys.path[0]+"/../")
from ixbrowser_local_api import IXBrowserClient, Proxy, Consts

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

"""
Randomly generate browser fingerprints and reassign a proxy
Mostly used for data crawlers, etc.

Required installation
pip install ixbrowser-local-api
pip install selenium

More information
https://github.com/ixspyinc/ixbrowser-local-api-python
"""

c = IXBrowserClient()
c.show_request_log = True

# Make sure the profile has been created
profile_id = 1

'''
p = Proxy()
p.proxy_mode = Consts.PROXY_MODE_CUSTOM
p.proxy_type = 'socks5'
p.proxy_ip = '192.168.7.96'
p.proxy_port = '20201'
open_result = c.open_profile_with_random_fingerprint(profile_id, load_profile_info_page=False, proxy_config=p)
'''
open_result = c.open_profile_with_random_fingerprint(profile_id, load_profile_info_page=False)
if open_result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Open profile error:')
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()

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
# If using selenium, it is recommended to use the following method to close
c.close_profile_via_selenium(driver)

print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'window closed.')



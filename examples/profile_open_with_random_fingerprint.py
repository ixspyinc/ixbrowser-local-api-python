import sys
import time
import random
from ixbrowser_local_api import IXBrowserClient, Proxy, Consts

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

c = IXBrowserClient()

# Make sure the profile has been created
profile_id = 251
p = Proxy()
p.proxy_mode = Consts.PROXY_MODE_CUSTOM
p.proxy_type = 'socks5'
p.proxy_ip = '192.168.7.96'
p.proxy_port = '20201'

open_result = c.open_profile_with_random_fingerprint(profile_id, load_profile_info_page=True, proxy_config=p)
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
driver.get("https://www.bing.com")
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

driver.close()
# driver.quit()

print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'window closed.')



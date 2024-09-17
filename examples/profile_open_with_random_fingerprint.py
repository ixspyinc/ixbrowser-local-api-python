import sys
import time
import random
sys.path.insert(0, sys.path[0]+"/../")
from ixbrowser_local_api import IXBrowserClient, Proxy, Consts, Fingerprint

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

# Allow partial fingerprints to specify values in random mode
f = Fingerprint()
f.ua_info = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
f.track= 0

open_result = c.open_profile_with_random_fingerprint(profile_id, load_profile_info_page=False, fingerprint_config=f)
if open_result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Open profile error:')
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()

'''
# Random fingerprint mode while modifying IP proxy
p = Proxy()
p.proxy_mode = Consts.PROXY_MODE_CUSTOM
p.proxy_type = 'socks5'
p.proxy_ip = '127.0.0.1'
p.proxy_port = '10808'
open_result = c.open_profile_with_random_fingerprint(profile_id, load_profile_info_page=False, proxy_config=p)
'''

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

# close profile
close_result = c.close_profile(profile_id)
if close_result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Close profile error:')
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()

print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'window closed.')

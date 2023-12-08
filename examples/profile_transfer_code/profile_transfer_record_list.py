import sys
import time
sys.path.insert(0, sys.path[0]+"/../../")
from ixbrowser_local_api import IXBrowserClient
from ixbrowser_local_api import Consts

c = IXBrowserClient()
c.show_request_log = True

record_type = Consts.TRANSFER_RECORD_LIST_TYPE_IMPORT
# record_type = Consts.TRANSFER_RECORD_LIST_TYPE_TRANSFER

result = c.get_profile_transfer_record_list(record_type=record_type)
print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Get Profile Transfer Record List:')
if result is None:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
    sys.exit()
else:
    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Result:')
    for item in result:
        for k in item:
            print(k, item[k])
        print()
        print('----------------')
        print()


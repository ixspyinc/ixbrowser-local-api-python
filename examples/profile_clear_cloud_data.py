import sys
import time
sys.path.insert(0, sys.path[0]+"/../")
from ixbrowser_local_api import IXBrowserClient, Consts

"""
Clear the cloud data of one or more profiles.

The data_type argument tells the client which kinds of cloud data should be
cleared, it can be a string or a list, and the optional values are:
    Consts.CLOUD_DATA_TYPE_INDEXED_DB     = 'indexed_db'
    Consts.CLOUD_DATA_TYPE_LOCAL_STORAGE  = 'local_storage'
    Consts.CLOUD_DATA_TYPE_EXTENSION_DATA = 'extension_data'

Required installation
pip install ixbrowser-local-api

More information
https://github.com/ixspyinc/ixbrowser-local-api-python
"""

c = IXBrowserClient()
c.show_request_log = True

# One profile id or a list of profile ids
profile_id = [1456, 1457]

# A single type or a list of types
data_type = [Consts.CLOUD_DATA_TYPE_INDEXED_DB,
             Consts.CLOUD_DATA_TYPE_LOCAL_STORAGE,
             Consts.CLOUD_DATA_TYPE_EXTENSION_DATA]
# data_type = Consts.CLOUD_DATA_TYPE_INDEXED_DB


def clear_cloud_data():
    result = c.clear_profile_cloud_data(profile_id, data_type)
    if result is None:
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Clear profile cloud data error:')
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
        return False

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Cleared profile id:', result)
    return True


if __name__ == '__main__':
    if not clear_cloud_data():
        sys.exit()

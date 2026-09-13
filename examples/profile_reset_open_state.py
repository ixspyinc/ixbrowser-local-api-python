import sys
import time
sys.path.insert(0, sys.path[0]+"/../")
from ixbrowser_local_api import IXBrowserClient

"""
Reset the open state of a profile.

Use it when a profile is still shown as opened in the client but it is actually
closed, for example after the browser process was killed or the machine restarted.

Required installation
pip install ixbrowser-local-api

More information
https://github.com/ixspyinc/ixbrowser-local-api-python
"""

c = IXBrowserClient()
c.show_request_log = True

# Make sure the profile has been created
profile_id = 1


def reset_open_state():
    result = c.reset_profile_open_state(profile_id)
    if result is None:
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Reset profile open state error:')
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
        return False

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'profile_id=', profile_id, 'result:', result)
    return True


def clear_saved_user_password():
    result = c.clear_profile_saved_user_password(profile_id)
    if result is None:
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Clear saved user password error:')
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error code=', c.code)
        print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'Error message=', c.message)
        return False

    print(time.strftime("%H:%M:%S", time.localtime(time.time())), 'profile_id=', profile_id, 'result:', result)
    return True


if __name__ == '__main__':
    # Only one of the two calls is needed, uncomment the one to use.

    if not reset_open_state():
        sys.exit()

    # if not clear_saved_user_password():
    #     sys.exit()

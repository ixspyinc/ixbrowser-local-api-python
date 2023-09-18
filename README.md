# ixBrowser Local API

ixBrowser local API official python version

## Installation

```BASH
pip install ixbrowser_local_api
```

## Usage

Basic usage
```python
c = IXBrowserClient()
data = c.get_profile_list()
if data is None:
    print('Get profile list error:')
    print('Error code=', c.code)
    print('Error message=', c.message)
else:
	item = random.choice(data)

	profile_id = item['profile_id']
	print('Random choice profile_id=', profile_id)

	open_result = c.open_profile(profile_id, cookies_backup=False, load_profile_info_page=False)
	if open_result is None:
		print('Open profile error:')
		print('Error code=', c.code)
		print('Error message=', c.message)
	else:
		print(open_result)
```

Advance use

For detailed usage, please refer to the files in the /examples directory.



Build
=====

```bash
git clone https://github.com/ixspyinc/ixbrowser-local-api-python
cd ixbrowser-local-api-python
python setup.py install
```

# ixBrowser Local API

ixBrowser本地API V2.0 Python版本

## README.md
- en [English](README.md)
- zh_CN [简体中文](README.zh_CN.md)

## 安装方法

1. pypi安装
```BASH
pip install ixbrowser-local-api
```

2. 源代码安装
```BASH
git clone https://github.com/ixspyinc/ixbrowser-local-api-python.git
cd ixbrowser-local-api-python
python setup.py install
```

## 使用方法

简单参考
```python
import random
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient()
data = c.get_profile_list()
if data is None:
    print('获取窗口列表错误:')
    print('错误代码=', c.code)
    print('错误描述=', c.message)
else:
	item = random.choice(data)

	profile_id = item['profile_id']
	print('随机打开窗口，窗口ID=', profile_id)

	open_result = c.open_profile(profile_id, cookies_backup=False, load_profile_info_page=False)
	if open_result is None:
		print('打开窗口错误:')
		print('错误代码=', c.code)
		print('错误描述=', c.message)
	else:
		print(open_result)
```

更多高级参考

/examples 目录中有更多使用范例



## API文档

https://www.ixbrowser.com/doc/v2/local-api/cn

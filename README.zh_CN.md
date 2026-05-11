# ixBrowser Local API

ixBrowser 本地 API V2.0 的官方 Python SDK。

## 语言

- [English](README.md)
- [简体中文](README.zh_CN.md)

## 使用前提

- 已安装并运行 ixBrowser 桌面客户端。
- 已在 ixBrowser 桌面客户端中启用本地 API 服务。
- 默认连接地址为 `http://127.0.0.1:53200/api/v2/`。
- Python 版本需为 3.5 或更高版本。

如果你的本地 API 使用了不同的主机或端口，可以在初始化客户端时传入：

```python
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient(target="127.0.0.1", port=53200)
```

## 安装方法

通过 PyPI 安装：

```bash
pip install ixbrowser-local-api
```

通过源码安装：

```bash
git clone https://github.com/ixspyinc/ixbrowser-local-api-python.git
cd ixbrowser-local-api-python
python setup.py install
```

## 快速开始

```python
import random
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient()

profiles = c.get_profile_list()
if profiles is None:
    print("获取窗口列表失败:")
    print("错误码=", c.code)
    print("错误信息=", c.message)
else:
    item = random.choice(profiles)
    profile_id = item["profile_id"]
    print("随机选择 profile_id=", profile_id)

    open_result = c.open_profile(
        profile_id,
        cookies_backup=False,
        load_profile_info_page=False,
    )
    if open_result is None:
        print("打开窗口失败:")
        print("错误码=", c.code)
        print("错误信息=", c.message)
    else:
        print(open_result)
        # open_result 包含 "webdriver" 和 "debugging_address" 字段。
        # 后续可用于接入 Selenium、Playwright 等浏览器自动化工具。
```

## 错误处理

大多数客户端方法在成功时返回 API 数据。请求失败时，方法会返回 `None`，错误详情保存在客户端实例的 `code` 和 `message` 字段中：

```python
result = c.get_profile_list()
if result is None:
    print(c.code)
    print(c.message)
```

## 更多文档

- [API 方法索引](docs/api-reference.md)
- [实体对象说明](docs/entities.md)
- [错误处理说明](docs/error-handling.md)
- [示例导航](examples/README.md)

## 示例

`examples/` 目录包含常见场景的可运行脚本：

- `examples/simple_test.py`：基础连通性和常用 API 调用。
- `examples/show_info.py`：展示本地信息和资源列表。
- `examples/profile_create.py`：创建窗口，并配置代理、偏好和指纹。
- `examples/profile_open.py`：打开窗口并接入 Selenium。
- `examples/profile_open_with_random_fingerprint.py`：使用随机指纹打开窗口。
- `examples/profile_update.py`：更新窗口配置。
- `examples/profile_copy.py`：复制已有窗口创建新窗口。
- `examples/tag/`：窗口标签增删改查示例。
- `examples/proxy_tag/`：代理标签增删改查示例。
- `examples/profile_transfer_code/`：窗口转移码相关示例。

完整说明请参考 [examples/README.md](examples/README.md)。

## 官方 API 文档

- 英文：https://www.ixbrowser.com/doc/v2/local-api/en
- 中文：https://www.ixbrowser.com/doc/v2/local-api/cn

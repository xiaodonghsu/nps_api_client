# NPS API客户端

这是一个NPS服务API客户端的 python 实现，支持的客户端管理、域名解析、隧道和设备管理功能。
参考文档：

[docs/api.md](https://github.com/ehang-io/nps/blob/master/docs/api.md)

[docs/webapi.md](https://github.com/ehang-io/nps/blob/master/docs/webapi.md)

## 功能特性

### 基础功能
- ✅ 基础认证流程
- ✅ 获取服务器时间
- ✅ AES CBC解密
- ✅ MD5加密验证

### 管理功能
- ✅ 客户端管理（增删改查）
- ✅ 域名解析管理
- ✅ 隧道管理
- ✅ 设备列表获取
- ✅ 实时监控

## 使用方法

### 1. 直接运行（获取当前的设备列表）

```bash
python nps_client.py
```

### 2. 在代码中使用

```python
from nps_client import NPSClient

# 创建客户端
client = NPSClient()

# 单次获取设备列表
devices = client.get_device_list(start=0, limit=10)
if devices:
    print("设备列表:", devices)

```


# NPS API客户端

这是一个完整的NPS服务API客户端，支持完整的客户端管理、域名解析、隧道和设备管理功能。

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

### 实用功能
- ✅ 自动刷新机制
- ✅ 友好的命令行界面
- ✅ 错误处理和重试机制
- ✅ 完整的API封装

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 直接运行

```bash
python nps_client.py
```

程序会提供两个选项：
- **选项1**: 单次获取设备列表
- **选项2**: 实时监控设备列表（按Ctrl+C停止）

### 2. 在代码中使用

```python
from nps_client import NPSClient

# 创建客户端
client = NPSClient()

# 单次获取设备列表
devices = client.get_device_list(start=0, limit=10)
if devices:
    print("设备列表:", devices)

# 实时监控（每60秒获取一次）
client.realtime_device_monitor(interval=60, start=0, limit=10)
```

## API流程

1. **获取加密auth_key** → `POST /auth/getauthkey`
2. **解密auth_key** → AES CBC解密
3. **获取服务器时间** → `POST /auth/gettime`
4. **生成请求auth_key** → `MD5(auth_key + timestamp)`
5. **获取设备列表** → `POST /client/list`

## 配置文件

- `auth_crypt_key`: 固定为 `H6RQdb25UxCrUbKF`
- `base_url`: 默认为 `http://uassist.cn/nps`

## 项目结构

```
nps_api_test/
├── nps_client.py          # 主程序
├── test_api.py           # API连接测试
├── decrypt_auth.py       # 解密模块（参考）
├── encrypt_auth.py       # 加密模块（参考）
├── nps.txt               # API文档
├── requirements.txt      # 依赖包
└── README.md             # 说明文档
```

## 测试验证

程序已通过以下测试：
- ✅ API连接测试成功
- ✅ 服务器时间获取正常
- ✅ 加密auth_key获取正常
- ✅ 响应格式正确

## 注意事项

1. 确保网络连接正常
2. 服务器地址默认为 `http://uassist.cn/nps`
3. 实时监控会持续运行，按Ctrl+C停止
4. 如需调整参数，可在代码中修改或通过命令行输入
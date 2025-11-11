#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NPS API客户端 - 完整的NPS服务管理工具
作者: AI Assistant
日期: 2025-11-11
"""

import requests
import hashlib
import time
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

class NPSClient:
    """NPS服务API客户端 - 支持完整的客户端、域名解析、隧道管理"""
    
    def __init__(self, base_url="http://uassist.cn/nps"):
        self.base_url = base_url
        self.auth_crypt_key = "H6RQdb25UxCrUbKF"
        
    def _get_auth_params(self):
        """获取认证参数 (auth_key, timestamp)"""
        try:
            # 1. 获取加密的auth_key
            encrypted_auth_key = self.get_encrypted_auth_key()
            if not encrypted_auth_key:
                return None, None
            
            # 2. 解密auth_key
            decrypted_auth_key = self.decrypt_auth_key(encrypted_auth_key)
            if not decrypted_auth_key:
                return None, None
            
            # 3. 获取服务器时间
            server_time = self.get_server_time()
            
            # 4. 生成请求用的auth_key
            request_auth_key = self.generate_request_auth_key(decrypted_auth_key, server_time)
            
            return request_auth_key, server_time
            
        except Exception as e:
            print(f"获取认证参数失败: {e}")
            return None, None
    
    def get_server_time(self):
        """获取服务器时间"""
        try:
            url = f"{self.base_url}/auth/gettime"
            response = requests.post(url)
            if response.status_code == 200:
                data = response.json()
                return data.get('time', int(time.time()))
            else:
                print(f"获取服务器时间失败: {response.status_code}")
                return int(time.time())
        except Exception as e:
            print(f"获取服务器时间异常: {e}")
            return int(time.time())
    
    def get_encrypted_auth_key(self):
        """获取加密后的auth_key"""
        try:
            url = f"{self.base_url}/auth/getauthkey"
            response = requests.post(url)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 1:
                    return data.get('crypt_auth_key')
                else:
                    print(f"获取auth_key失败，状态码: {data.get('status')}")
                    return None
            else:
                print(f"请求失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取加密auth_key异常: {e}")
            return None
    
    def decrypt_auth_key(self, encrypted_hex):
        """解密auth_key"""
        try:
            # 将十六进制字符串转换为字节
            encrypted_bytes = binascii.unhexlify(encrypted_hex)
            
            # 填充密钥到16字节
            padded_key = self.auth_crypt_key.ljust(16, '\x00')
            
            # 使用密钥作为IV（偏移量与密钥相同）
            iv = padded_key.encode('utf-8')
            
            # 获取加密数据（整个字节串都是密文）
            ciphertext = encrypted_bytes
            
            # 创建AES CBC解密器
            cipher = AES.new(padded_key.encode('utf-8'), AES.MODE_CBC, iv)
            
            # 解密并去除PKCS5填充
            decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
            
            # 转换为字符串
            auth_key = decrypted_data.decode('utf-8')
            
            return auth_key
        except Exception as e:
            print(f"解密auth_key失败: {e}")
            return None
    
    def generate_request_auth_key(self, auth_key, timestamp):
        """生成请求用的auth_key (md5(auth_key + timestamp))"""
        try:
            # 拼接字符串并计算MD5
            raw_string = auth_key + str(timestamp)
            md5_hash = hashlib.md5(raw_string.encode('utf-8')).hexdigest()
            return md5_hash
        except Exception as e:
            print(f"生成请求auth_key失败: {e}")
            return None
    
    # ========== 客户端管理 ==========
    
    def get_client_list(self, search="", order="asc", offset=0, limit=10):
        """获取客户端列表"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/client/list/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'search': search,
            'order': order,
            'offset': offset,
            'limit': limit
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取客户端列表失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取客户端列表异常: {e}")
            return None
    
    def get_client(self, client_id):
        """获取单个客户端信息"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/client/getclient/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'id': client_id
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取客户端信息失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取客户端信息异常: {e}")
            return None
    
    def add_client(self, remark, u="", p="", vkey="", config_conn_allow=1, 
                   compress=0, crypt=0, rate_limit="", flow_limit="", 
                   max_conn="", max_tunnel=""):
        """添加客户端"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/client/add/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'remark': remark,
            'u': u,
            'p': p,
            'vkey': vkey,
            'config_conn_allow': config_conn_allow,
            'compress': compress,
            'crypt': crypt,
            'rate_limit': rate_limit,
            'flow_limit': flow_limit,
            'max_conn': max_conn,
            'max_tunnel': max_tunnel
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"添加客户端失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"添加客户端异常: {e}")
            return None
    
    def edit_client(self, client_id, remark, u="", p="", vkey="", config_conn_allow=1,
                    compress=0, crypt=0, rate_limit="", flow_limit="", 
                    max_conn="", max_tunnel=""):
        """修改客户端"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/client/edit/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'id': client_id,
            'remark': remark,
            'u': u,
            'p': p,
            'vkey': vkey,
            'config_conn_allow': config_conn_allow,
            'compress': compress,
            'crypt': crypt,
            'rate_limit': rate_limit,
            'flow_limit': flow_limit,
            'max_conn': max_conn,
            'max_tunnel': max_tunnel
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"修改客户端失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"修改客户端异常: {e}")
            return None
    
    def delete_client(self, client_id):
        """删除客户端"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/client/del/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'id': client_id
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"删除客户端失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"删除客户端异常: {e}")
            return None
    
    # ========== 域名解析管理 ==========
    
    def get_host_list(self, search="", offset=0, limit=10):
        """获取域名解析列表"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/index/hostlist/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'search': search,
            'offset': offset,
            'limit': limit
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取域名解析列表失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取域名解析列表异常: {e}")
            return None
    
    def add_host(self, remark, host, scheme="all", location="", client_id="", 
                 target="", header="", hostchange=""):
        """添加域名解析"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/index/addhost/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'remark': remark,
            'host': host,
            'scheme': scheme,
            'location': location,
            'client_id': client_id,
            'target': target,
            'header': header,
            'hostchange': hostchange
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"添加域名解析失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"添加域名解析异常: {e}")
            return None
    
    def edit_host(self, host_id, remark, host, scheme="all", location="", 
                  client_id="", target="", header="", hostchange=""):
        """修改域名解析"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/index/edithost/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'id': host_id,
            'remark': remark,
            'host': host,
            'scheme': scheme,
            'location': location,
            'client_id': client_id,
            'target': target,
            'header': header,
            'hostchange': hostchange
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"修改域名解析失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"修改域名解析异常: {e}")
            return None
    
    def delete_host(self, host_id):
        """删除域名解析"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/index/delhost/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'id': host_id
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"删除域名解析失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"删除域名解析异常: {e}")
            return None
    
    # ========== 隧道管理 ==========
    
    def get_tunnel_info(self, tunnel_id):
        """获取单条隧道信息"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/index/getonetunnel/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'id': tunnel_id
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取隧道信息失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取隧道信息异常: {e}")
            return None
    
    def get_tunnel_list(self, client_id="", tunnel_type="", search="", offset=0, limit=10):
        """获取隧道列表"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/index/gettunnel/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'client_id': client_id,
            'type': tunnel_type,
            'search': search,
            'offset': offset,
            'limit': limit
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取隧道列表失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"获取隧道列表异常: {e}")
            return None
    
    def add_tunnel(self, tunnel_type, remark, port, target, client_id):
        """添加隧道"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/index/add/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'type': tunnel_type,
            'remark': remark,
            'port': port,
            'target': target,
            'client_id': client_id
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"添加隧道失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"添加隧道异常: {e}")
            return None
    
    def edit_tunnel(self, tunnel_id, tunnel_type, remark, port, target, client_id):
        """修改隧道"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/index/edit/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'id': tunnel_id,
            'type': tunnel_type,
            'remark': remark,
            'port': port,
            'target': target,
            'client_id': client_id
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"修改隧道失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"修改隧道异常: {e}")
            return None
    
    def delete_tunnel(self, tunnel_id):
        """删除隧道"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/index/del/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'id': tunnel_id
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"删除隧道失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"删除隧道异常: {e}")
            return None
    
    def start_tunnel(self, tunnel_id):
        """隧道开始工作"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/index/start/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'id': tunnel_id
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"启动隧道失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"启动隧道异常: {e}")
            return None
    
    def stop_tunnel(self, tunnel_id):
        """隧道停止工作"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        url = f"{self.base_url}/index/stop/"
        data = {
            'auth_key': auth_key,
            'timestamp': timestamp,
            'id': tunnel_id
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"停止隧道失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"停止隧道异常: {e}")
            return None
    
    # ========== 向后兼容的方法 ==========
    
    def get_device_list(self, start=0, limit=10):
        """获取设备列表（向后兼容）"""
        auth_key, timestamp = self._get_auth_params()
        if not auth_key:
            return None
            
        try:
            # 获取解密后的auth_key用于显示
            encrypted_auth = self.get_encrypted_auth_key()
            if encrypted_auth:
                decrypted_auth = self.decrypt_auth_key(encrypted_auth)
                print(f"解密后的auth_key: {decrypted_auth}")
            
            print(f"服务器时间: {timestamp}")
            print(f"请求用的auth_key: {auth_key}")
            
            # 发送获取设备列表的请求
            url = f"{self.base_url}/client/list"
            data = {
                'auth_key': auth_key,
                'timestamp': timestamp,
                'start': start,
                'limit': limit
            }
            
            response = requests.post(url, data=data)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"获取设备列表失败: {response.status_code}")
                print(f"响应内容: {response.text}")
                return None
                
        except Exception as e:
            print(f"获取设备列表异常: {e}")
            return None

def main():
    """主函数"""
    client = NPSClient()
    
    print("NPS API客户端")

    try:
        result = client.get_device_list()
        if result:
            print("\n设备列表:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("获取设备列表失败")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试数据格式脚本
"""

import requests
import json

def test_spot_price_api():
    """测试抢占式实例价格API"""
    
    # 测试数据
    test_data = {
        "zone_id": "cn-qingdao-b",
        "instance_types": ["ecs.t1.small"],
        "network_type": "vpc",
        "os_type": "linux",
        "io_optimized": "optimized"
    }
    
    try:
        # 发送请求
        response = requests.post(
            "http://localhost:8000/api/spot-price-history",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # 检查数据结构
            if 'data' in data and data['data']:
                print(f"\n数据条数: {len(data['data'])}")
                print(f"第一条数据: {data['data'][0]}")
                
                # 检查时间戳格式
                for item in data['data']:
                    print(f"时间戳: {item.get('timestamp')}")
                    print(f"价格: {item.get('spot_price')}")
                    print(f"实例类型: {item.get('instance_type')}")
                    break
            else:
                print("没有数据返回")
        else:
            print(f"错误响应: {response.text}")
            
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    test_spot_price_api() 
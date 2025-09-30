#!/usr/bin/env python3
"""
测试API接口
"""
import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    try:
        # 测试exercises接口
        print("🔍 测试 /api/v1/exercises/ 接口...")
        response = requests.get(f"{base_url}/api/v1/exercises/?limit=2")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"返回数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        else:
            print(f"错误响应: {response.text}")
        
        # 测试统计接口
        print("\n🔍 测试 /api/v1/exercises/statistics/overview 接口...")
        response = requests.get(f"{base_url}/api/v1/exercises/statistics/overview")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"统计数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        else:
            print(f"错误响应: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_api()


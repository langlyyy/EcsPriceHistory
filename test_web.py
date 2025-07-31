#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web版本测试脚本
测试前后端分离架构的各个组件
"""

import requests
import json
import time
import sys
import os

def test_backend_health():
    """测试后端健康检查"""
    print("🔍 测试后端健康检查...")
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务运行正常")
            return True
        else:
            print(f"❌ 后端服务异常，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到后端服务: {e}")
        return False

def test_api_endpoints():
    """测试API接口"""
    print("\n🔍 测试API接口...")
    
    # 测试根路径
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ 根路径API正常")
        else:
            print(f"❌ 根路径API异常，状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 根路径API测试失败: {e}")
    
    # 测试地域列表API
    try:
        response = requests.get("http://localhost:8000/api/regions", timeout=10)
        if response.status_code == 200:
            regions = response.json()
            print(f"✅ 地域列表API正常，获取到 {len(regions)} 个地域")
        else:
            print(f"❌ 地域列表API异常，状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 地域列表API测试失败: {e}")

def test_frontend_proxy():
    """测试前端代理配置"""
    print("\n🔍 测试前端代理配置...")
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ 前端服务运行正常")
            return True
        else:
            print(f"❌ 前端服务异常，状态码: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 无法连接到前端服务: {e}")
        print("💡 提示: 请先启动前端服务 (npm run dev)")
        return False

def check_dependencies():
    """检查依赖"""
    print("🔍 检查依赖...")
    
    # 检查Python依赖
    try:
        import fastapi
        import uvicorn
        import aliyunsdkcore
        import aliyunsdkecs
        print("✅ Python依赖检查通过")
    except ImportError as e:
        print(f"❌ Python依赖缺失: {e}")
        return False
    
    # 检查Node.js依赖
    if os.path.exists("frontend/node_modules"):
        print("✅ Node.js依赖已安装")
    else:
        print("⚠️  Node.js依赖未安装，请运行: cd frontend && npm install")
        return False
    
    return True

def main():
    """主测试函数"""
    print("=" * 60)
    print("阿里云抢占式实例价格查询工具 - Web版本测试")
    print("=" * 60)
    
    # 检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败，请先安装依赖")
        return
    
    # 等待后端启动
    print("\n⏳ 等待后端服务启动...")
    time.sleep(3)
    
    # 测试后端
    if not test_backend_health():
        print("\n❌ 后端服务未启动，请先启动后端服务")
        print("💡 启动命令: cd backend && python main.py")
        return
    
    # 测试API接口
    test_api_endpoints()
    
    # 测试前端
    if test_frontend_proxy():
        print("\n🎉 所有测试通过！")
        print("\n📱 访问地址:")
        print("   前端应用: http://localhost:3000")
        print("   API文档:  http://localhost:8000/docs")
        print("   后端健康检查: http://localhost:8000/api/health")
    else:
        print("\n⚠️  前端服务未启动，请启动前端服务")
        print("💡 启动命令: cd frontend && npm run dev")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main() 
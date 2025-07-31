#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Docker 配置测试脚本
用于验证 Docker 部署配置是否正确
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_status(message, status="INFO"):
    """打印状态信息"""
    colors = {
        "INFO": "\033[94m",    # 蓝色
        "SUCCESS": "\033[92m", # 绿色
        "WARNING": "\033[93m", # 黄色
        "ERROR": "\033[91m",   # 红色
        "RESET": "\033[0m"     # 重置
    }
    print(f"{colors.get(status, colors['INFO'])}[{status}]{colors['RESET']} {message}")

def check_docker_installation():
    """检查 Docker 是否安装"""
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, check=True)
        print_status(f"Docker 已安装: {result.stdout.strip()}", "SUCCESS")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_status("Docker 未安装或未在 PATH 中", "ERROR")
        return False

def check_docker_compose():
    """检查 Docker Compose 是否安装"""
    try:
        result = subprocess.run(['docker-compose', '--version'], 
                              capture_output=True, text=True, check=True)
        print_status(f"Docker Compose 已安装: {result.stdout.strip()}", "SUCCESS")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_status("Docker Compose 未安装或未在 PATH 中", "ERROR")
        return False

def check_docker_daemon():
    """检查 Docker 守护进程是否运行"""
    try:
        result = subprocess.run(['docker', 'info'], 
                              capture_output=True, text=True, check=True)
        print_status("Docker 守护进程正在运行", "SUCCESS")
        return True
    except subprocess.CalledProcessError:
        print_status("Docker 守护进程未运行", "ERROR")
        return False

def check_required_files():
    """检查必需的文件是否存在"""
    required_files = [
        "docker-compose.yml",
        "backend/Dockerfile",
        "frontend/Dockerfile",
        "backend/config.py",
        "backend/requirements.txt",
        "frontend/package.json",
        "frontend/nginx.conf"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print_status(f"✓ {file_path}", "SUCCESS")
        else:
            print_status(f"✗ {file_path}", "ERROR")
            missing_files.append(file_path)
    
    return len(missing_files) == 0

def check_backend_config():
    """检查后端配置"""
    config_file = "backend/config.py"
    if not os.path.exists(config_file):
        print_status("后端配置文件不存在", "ERROR")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查是否包含API密钥配置
        if "ALIYUN_ACCESS_KEY_ID" in content and "ALIYUN_ACCESS_KEY_SECRET" in content:
            print_status("后端配置文件包含API密钥配置", "SUCCESS")
            return True
        else:
            print_status("后端配置文件缺少API密钥配置", "WARNING")
            return False
    except Exception as e:
        print_status(f"读取配置文件失败: {e}", "ERROR")
        return False

def validate_docker_compose():
    """验证 docker-compose.yml 文件"""
    try:
        result = subprocess.run(['docker-compose', 'config'], 
                              capture_output=True, text=True, check=True)
        print_status("docker-compose.yml 配置有效", "SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print_status(f"docker-compose.yml 配置无效: {e.stderr}", "ERROR")
        return False

def test_docker_build():
    """测试 Docker 构建"""
    print_status("开始测试 Docker 构建...")
    
    try:
        # 测试后端构建
        print_status("测试后端镜像构建...")
        result = subprocess.run(['docker-compose', 'build', 'backend'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print_status("后端镜像构建成功", "SUCCESS")
        else:
            print_status(f"后端镜像构建失败: {result.stderr}", "ERROR")
            return False
        
        # 测试前端构建
        print_status("测试前端镜像构建...")
        result = subprocess.run(['docker-compose', 'build', 'frontend'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print_status("前端镜像构建成功", "SUCCESS")
            return True
        else:
            print_status(f"前端镜像构建失败: {result.stderr}", "ERROR")
            return False
            
    except subprocess.TimeoutExpired:
        print_status("构建超时", "ERROR")
        return False
    except Exception as e:
        print_status(f"构建测试失败: {e}", "ERROR")
        return False

def main():
    """主函数"""
    print_status("开始 Docker 配置测试", "INFO")
    print_status("=" * 50, "INFO")
    
    tests = [
        ("Docker 安装检查", check_docker_installation),
        ("Docker Compose 检查", check_docker_compose),
        ("Docker 守护进程检查", check_docker_daemon),
        ("必需文件检查", check_required_files),
        ("后端配置检查", check_backend_config),
        ("Docker Compose 配置验证", validate_docker_compose),
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print_status(f"\n执行测试: {test_name}", "INFO")
        if test_func():
            passed_tests += 1
    
    print_status("=" * 50, "INFO")
    print_status(f"测试结果: {passed_tests}/{total_tests} 通过", 
                "SUCCESS" if passed_tests == total_tests else "WARNING")
    
    if passed_tests == total_tests:
        print_status("\n所有基础测试通过！可以尝试构建测试...", "INFO")
        
        # 询问是否进行构建测试
        try:
            response = input("\n是否进行 Docker 构建测试？(y/N): ").strip().lower()
            if response in ['y', 'yes']:
                if test_docker_build():
                    print_status("Docker 构建测试通过！", "SUCCESS")
                    print_status("可以开始部署了！", "SUCCESS")
                else:
                    print_status("Docker 构建测试失败", "ERROR")
            else:
                print_status("跳过构建测试", "INFO")
        except KeyboardInterrupt:
            print_status("\n用户取消构建测试", "INFO")
    else:
        print_status("请修复上述问题后重试", "ERROR")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_status("\n测试被用户中断", "WARNING")
        sys.exit(1)
    except Exception as e:
        print_status(f"测试过程中发生错误: {e}", "ERROR")
        sys.exit(1) 
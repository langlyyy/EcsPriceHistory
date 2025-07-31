#!/bin/bash

# 阿里云抢占式实例价格查询工具 - Docker部署脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  阿里云抢占式实例价格查询工具${NC}"
    echo -e "${BLUE}        Docker 部署脚本${NC}"
    echo -e "${BLUE}================================${NC}"
}

# 检查Docker是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    print_message "Docker 和 Docker Compose 已安装"
}

# 检查配置文件
check_config() {
    if [ ! -f "backend/config.py" ]; then
        print_error "后端配置文件 backend/config.py 不存在"
        exit 1
    fi
    
    print_message "配置文件检查完成"
}

# 构建镜像
build_images() {
    print_message "开始构建 Docker 镜像..."
    
    # 构建后端镜像
    print_message "构建后端镜像..."
    docker-compose build backend
    
    # 构建前端镜像
    print_message "构建前端镜像..."
    docker-compose build frontend
    
    print_message "镜像构建完成"
}

# 启动服务
start_services() {
    print_message "启动服务..."
    
    # 停止现有服务
    docker-compose down
    
    # 启动服务
    docker-compose up -d
    
    print_message "服务启动完成"
}

# 检查服务状态
check_services() {
    print_message "检查服务状态..."
    
    # 等待服务启动
    sleep 10
    
    # 检查容器状态
    docker-compose ps
    
    # 检查健康状态
    print_message "检查健康状态..."
    docker-compose exec backend curl -f http://localhost:8000/api/health || print_warning "后端健康检查失败"
    docker-compose exec frontend curl -f http://localhost:80 || print_warning "前端健康检查失败"
}

# 显示访问信息
show_access_info() {
    print_message "部署完成！"
    echo ""
    echo -e "${GREEN}访问地址:${NC}"
    echo -e "  前端: ${BLUE}http://localhost${NC}"
    echo -e "  后端API: ${BLUE}http://localhost:8000${NC}"
    echo -e "  API文档: ${BLUE}http://localhost:8000/docs${NC}"
    echo ""
    echo -e "${GREEN}常用命令:${NC}"
    echo -e "  查看日志: ${YELLOW}docker-compose logs -f${NC}"
    echo -e "  停止服务: ${YELLOW}docker-compose down${NC}"
    echo -e "  重启服务: ${YELLOW}docker-compose restart${NC}"
    echo -e "  查看状态: ${YELLOW}docker-compose ps${NC}"
}

# 生产环境部署
deploy_production() {
    print_message "开始生产环境部署..."
    
    # 使用生产环境配置
    docker-compose -f docker-compose.prod.yml down
    docker-compose -f docker-compose.prod.yml build
    docker-compose -f docker-compose.prod.yml up -d
    
    print_message "生产环境部署完成"
}

# 主函数
main() {
    print_header
    
    # 检查参数
    if [ "$1" = "prod" ]; then
        print_message "生产环境部署模式"
        check_docker
        check_config
        deploy_production
    else
        print_message "开发环境部署模式"
        check_docker
        check_config
        build_images
        start_services
        check_services
    fi
    
    show_access_info
}

# 脚本入口
main "$@" 
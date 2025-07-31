# Docker 部署指南

## 概述

本项目提供了完整的 Docker 部署方案，支持开发环境和生产环境的快速部署。

## 系统要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 2GB 可用内存
- 至少 5GB 可用磁盘空间

## 快速开始

### 1. 环境准备

确保已安装 Docker 和 Docker Compose：

```bash
# 检查 Docker 版本
docker --version

# 检查 Docker Compose 版本
docker-compose --version
```

### 2. 配置阿里云 API

编辑 `backend/config.py` 文件，配置你的阿里云 API 密钥：

```python
# 阿里云 API 配置
ALIYUN_ACCESS_KEY_ID = "your_access_key_id"
ALIYUN_ACCESS_KEY_SECRET = "your_access_key_secret"
```

### 3. 一键部署

#### Linux/Mac 用户：
```bash
# 给脚本执行权限
chmod +x deploy.sh

# 开发环境部署
./deploy.sh

# 生产环境部署
./deploy.sh prod
```

#### Windows 用户：
```cmd
# 开发环境部署
deploy.bat

# 生产环境部署
deploy.bat prod
```

### 4. 手动部署

如果不想使用自动部署脚本，可以手动执行：

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

## 服务架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Redis         │
│   (Nginx)       │    │   (FastAPI)     │    │   (Cache)       │
│   Port: 80      │◄──►│   Port: 8000    │◄──►│   Port: 6379    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 服务说明

- **Frontend**: Vue.js 前端应用，使用 Nginx 提供静态文件服务
- **Backend**: FastAPI 后端服务，提供 RESTful API
- **Redis**: 缓存服务，用于提高 API 响应速度（可选）

## 访问地址

部署完成后，可以通过以下地址访问：

- **前端应用**: http://localhost
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **Redis 管理**: http://localhost:6379 (需要 Redis 客户端)

## 常用命令

### 服务管理

```bash
# 启动所有服务
docker-compose up -d

# 停止所有服务
docker-compose down

# 重启所有服务
docker-compose restart

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 镜像管理

```bash
# 重新构建镜像
docker-compose build

# 重新构建特定服务
docker-compose build backend
docker-compose build frontend

# 强制重新构建（不使用缓存）
docker-compose build --no-cache
```

### 数据管理

```bash
# 查看数据卷
docker volume ls

# 清理数据卷
docker-compose down -v

# 备份数据
docker run --rm -v spot-price-history_redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis_backup.tar.gz -C /data .
```

## 环境配置

### 开发环境 (docker-compose.yml)

- 支持热重载
- 代码卷挂载
- 调试模式

### 生产环境 (docker-compose.prod.yml)

- 优化性能
- 移除开发依赖
- 安全配置

## 性能优化

### 1. 镜像优化

- 使用多阶段构建
- 最小化镜像大小
- 优化依赖安装

### 2. 网络优化

- 使用自定义网络
- 配置健康检查
- 优化代理设置

### 3. 缓存优化

- Redis 缓存 API 响应
- Nginx 静态文件缓存
- Docker 层缓存

## 安全配置

### 1. 网络安全

- 使用自定义网络隔离
- 限制端口暴露
- 配置防火墙规则

### 2. 应用安全

- 安全头配置
- CORS 策略
- 输入验证

### 3. 数据安全

- 敏感信息环境变量化
- 数据卷权限控制
- 定期备份

## 监控和日志

### 1. 健康检查

所有服务都配置了健康检查：

```bash
# 查看健康状态
docker-compose ps

# 手动健康检查
curl http://localhost:8000/api/health
curl http://localhost:80
```

### 2. 日志管理

```bash
# 查看所有日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 导出日志
docker-compose logs > app.log
```

### 3. 性能监控

```bash
# 查看资源使用情况
docker stats

# 查看容器详细信息
docker inspect spot-price-backend
docker inspect spot-price-frontend
```

## 故障排除

### 常见问题

1. **端口冲突**
   ```bash
   # 检查端口占用
   netstat -tulpn | grep :80
   netstat -tulpn | grep :8000
   
   # 修改端口映射
   # 编辑 docker-compose.yml
   ports:
     - "8080:80"  # 改为 8080
   ```

2. **内存不足**
   ```bash
   # 增加 Docker 内存限制
   # 在 Docker Desktop 设置中调整
   ```

3. **构建失败**
   ```bash
   # 清理缓存重新构建
   docker-compose build --no-cache
   
   # 清理 Docker 系统
   docker system prune -a
   ```

4. **服务无法启动**
   ```bash
   # 查看详细错误信息
   docker-compose logs backend
   docker-compose logs frontend
   
   # 检查配置文件
   cat backend/config.py
   ```

### 调试模式

```bash
# 以调试模式启动
docker-compose up

# 进入容器调试
docker-compose exec backend bash
docker-compose exec frontend sh
```

## 扩展部署

### 1. 多实例部署

```bash
# 扩展后端服务
docker-compose up -d --scale backend=3

# 使用负载均衡器
# 配置 Nginx 负载均衡
```

### 2. 数据库集成

```bash
# 添加 PostgreSQL
# 在 docker-compose.yml 中添加：
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: spot_price
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

### 3. 反向代理

```bash
# 使用 Traefik
# 在 docker-compose.yml 中添加：
services:
  traefik:
    image: traefik:v2.5
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
    ports:
      - "80:80"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

## 备份和恢复

### 1. 数据备份

```bash
# 备份 Redis 数据
docker run --rm -v spot-price-history_redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis_backup_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .

# 备份配置文件
tar czf config_backup_$(date +%Y%m%d_%H%M%S).tar.gz backend/config.py
```

### 2. 数据恢复

```bash
# 恢复 Redis 数据
docker run --rm -v spot-price-history_redis_data:/data -v $(pwd):/backup alpine tar xzf /backup/redis_backup_20240101_120000.tar.gz -C /data

# 恢复配置文件
tar xzf config_backup_20240101_120000.tar.gz
```

## 更新部署

### 1. 代码更新

```bash
# 拉取最新代码
git pull

# 重新构建并部署
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 2. 配置更新

```bash
# 更新配置文件
vim backend/config.py

# 重启服务
docker-compose restart backend
```

### 3. 版本回滚

```bash
# 回滚到指定版本
git checkout v1.0.0

# 重新部署
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 联系支持

如果在部署过程中遇到问题，请：

1. 查看日志文件
2. 检查配置文件
3. 确认系统要求
4. 提交 Issue 到项目仓库

---

**注意**: 请确保在生产环境中正确配置安全设置，包括防火墙、SSL 证书等。 
@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM 阿里云抢占式实例价格查询工具 - Docker部署脚本 (Windows)

echo ================================
echo   阿里云抢占式实例价格查询工具
echo        Docker 部署脚本
echo ================================
echo.

REM 检查Docker是否安装
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker 未安装，请先安装 Docker Desktop
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose 未安装，请先安装 Docker Compose
    pause
    exit /b 1
)

echo [INFO] Docker 和 Docker Compose 已安装
echo.

REM 检查配置文件
if not exist "backend\config.py" (
    echo [ERROR] 后端配置文件 backend\config.py 不存在
    pause
    exit /b 1
)

echo [INFO] 配置文件检查完成
echo.

REM 检查参数
if "%1"=="prod" (
    echo [INFO] 生产环境部署模式
    goto :deploy_production
) else (
    echo [INFO] 开发环境部署模式
    goto :deploy_development
)

:deploy_development
echo [INFO] 开始构建 Docker 镜像...
echo.

echo [INFO] 构建后端镜像...
docker-compose build backend
if errorlevel 1 (
    echo [ERROR] 后端镜像构建失败
    pause
    exit /b 1
)

echo [INFO] 构建前端镜像...
docker-compose build frontend
if errorlevel 1 (
    echo [ERROR] 前端镜像构建失败
    pause
    exit /b 1
)

echo [INFO] 镜像构建完成
echo.

echo [INFO] 启动服务...
docker-compose down
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] 服务启动失败
    pause
    exit /b 1
)

echo [INFO] 服务启动完成
echo.

echo [INFO] 等待服务启动...
timeout /t 10 /nobreak >nul

echo [INFO] 检查服务状态...
docker-compose ps
echo.

goto :show_info

:deploy_production
echo [INFO] 开始生产环境部署...
echo.

docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build
if errorlevel 1 (
    echo [ERROR] 生产环境镜像构建失败
    pause
    exit /b 1
)

docker-compose -f docker-compose.prod.yml up -d
if errorlevel 1 (
    echo [ERROR] 生产环境服务启动失败
    pause
    exit /b 1
)

echo [INFO] 生产环境部署完成
echo.

:show_info
echo [INFO] 部署完成！
echo.
echo 访问地址:
echo   前端: http://localhost
echo   后端API: http://localhost:8000
echo   API文档: http://localhost:8000/docs
echo.
echo 常用命令:
echo   查看日志: docker-compose logs -f
echo   停止服务: docker-compose down
echo   重启服务: docker-compose restart
echo   查看状态: docker-compose ps
echo.
pause 
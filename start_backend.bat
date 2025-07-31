@echo off
echo 启动阿里云抢占式实例价格查询后端服务...
echo.

cd backend
echo 安装后端依赖...
pip install -r requirements.txt

echo.
echo 启动后端服务...
python main.py

pause 
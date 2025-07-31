@echo off
echo 启动阿里云抢占式实例价格查询前端服务...
echo.

cd frontend
echo 安装前端依赖...
npm install

echo.
echo 启动前端开发服务器...
npm run dev

pause 
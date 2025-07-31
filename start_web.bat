@echo off
echo ========================================
echo 阿里云抢占式实例价格查询工具 - Web版本
echo ========================================
echo.

echo 正在启动后端服务...
start "后端服务" cmd /k "cd backend && pip install -r requirements.txt && python main.py"

echo 等待后端服务启动...
timeout /t 5 /nobreak > nul

echo 正在启动前端服务...
start "前端服务" cmd /k "cd frontend && npm install && npm run dev"

echo.
echo ========================================
echo 服务启动完成！
echo ========================================
echo 后端服务: http://localhost:8000
echo 前端服务: http://localhost:3000
echo API文档: http://localhost:8000/docs
echo ========================================
echo.
echo 请在浏览器中打开 http://localhost:3000 使用应用
echo 按任意键退出...
pause > nul 
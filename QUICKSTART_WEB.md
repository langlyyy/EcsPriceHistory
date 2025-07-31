# Web版本快速启动指南

## 🚀 5分钟快速体验

### 方法一：一键启动（推荐）
```bash
# Windows用户
start_web.bat
```

### 方法二：分步启动

#### 1. 配置API密钥
编辑 `backend/config.py` 文件：
```python
ACCESS_KEY = "您的AccessKey"
ACCESS_SECRET = "您的AccessSecret"
```

#### 2. 启动后端
```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### 3. 启动前端
```bash
cd frontend
npm install
npm run dev
```

#### 4. 访问应用
打开浏览器访问：`http://localhost:3000`

## 📋 环境要求

- **Python**: 3.7+
- **Node.js**: 16+
- **浏览器**: Chrome, Firefox, Safari, Edge

## 🔧 常见问题

### Q: 如何获取阿里云API密钥？
A: 
1. 登录阿里云控制台
2. 点击右上角头像 → "AccessKey管理"
3. 创建AccessKey和AccessSecret

### Q: 前端无法连接后端？
A: 
1. 确认后端是否在8000端口运行
2. 检查 `frontend/vite.config.js` 代理配置
3. 确认CORS设置

### Q: 依赖安装失败？
A: 
1. 更新pip: `pip install --upgrade pip`
2. 更新npm: `npm install -g npm@latest`
3. 清除缓存: `npm cache clean --force`

## 📱 功能预览

- ✅ 地域和可用区选择
- ✅ 多实例规格对比
- ✅ 网络类型筛选
- ✅ 时间范围查询
- ✅ 价格趋势图表
- ✅ 数据导出功能

## 🔗 相关链接

- **应用地址**: http://localhost:3000
- **API文档**: http://localhost:8000/docs
- **后端健康检查**: http://localhost:8000/api/health 
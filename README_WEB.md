# 阿里云抢占式实例价格查询工具

## 项目简介
这是一个基于前后端分离架构的阿里云抢占式实例价格查询工具，提供现代化的Web界面，支持多规格对比和价格趋势分析。

## 技术架构

### 后端 (FastAPI)
- **框架**: FastAPI
- **语言**: Python 3.7+
- **主要功能**: 
  - 阿里云API调用
  - RESTful API接口
  - 数据验证和序列化
  - CORS支持

### 前端 (Vue.js)
- **框架**: Vue 3 + Vite
- **UI库**: Element Plus
- **图表库**: ECharts (待集成)
- **主要功能**:
  - 响应式用户界面
  - 实时数据查询
  - 价格趋势图表
  - 数据导出功能

## 快速开始

### 环境要求
- Python 3.7+
- Node.js 16+
- 阿里云账号和API密钥

### 安装和运行

#### 1. 配置API密钥
编辑 `backend/config.py` 文件，填入您的阿里云API密钥：
```python
ACCESS_KEY = "您的AccessKey"
ACCESS_SECRET = "您的AccessSecret"
```

#### 2. 启动后端服务
```bash
# Windows
start_backend.bat

# Linux/Mac
cd backend
pip install -r requirements.txt
python main.py
```

后端服务将在 `http://localhost:8000` 启动

#### 3. 启动前端服务
```bash
# Windows
start_frontend.bat

# Linux/Mac
cd frontend
npm install
npm run dev
```

前端服务将在 `http://localhost:3000` 启动

#### 4. 访问应用
在浏览器中打开 `http://localhost:3000` 即可使用应用

## API接口说明

### 基础信息
- **基础URL**: `http://localhost:8000`
- **API文档**: `http://localhost:8000/docs` (Swagger UI)

### 主要接口

#### 1. 获取地域列表
```
GET /api/regions
```

#### 2. 获取可用区列表
```
GET /api/zones/{region_id}
```

#### 3. 获取实例规格列表
```
GET /api/instance-types/{region_id}
```

#### 4. 获取抢占式实例价格历史
```
POST /api/spot-price-history
```

请求体示例：
```json
{
  "zone_id": "cn-hangzhou-b",
  "instance_types": ["ecs.g6.large", "ecs.c6.large"],
  "network_type": "vpc",
  "start_time": "2024-01-01T00:00:00Z",
  "end_time": "2024-01-02T00:00:00Z",
  "io_optimized": "optimized",
  "os_type": "linux"
}
```

## 项目结构

```
DescribeSpotPriceHistory/
├── backend/                 # 后端代码
│   ├── main.py             # FastAPI主应用
│   ├── aliyun_api.py       # 阿里云API调用
│   ├── models.py           # 数据模型
│   ├── config.py           # 配置文件
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── main.js         # Vue应用入口
│   │   ├── App.vue         # 主应用组件
│   │   ├── api/            # API服务
│   │   ├── router/         # 路由配置
│   │   └── views/          # 页面组件
│   ├── package.json        # Node.js依赖
│   ├── vite.config.js      # Vite配置
│   └── index.html          # HTML入口
├── start_backend.bat       # 后端启动脚本(Windows)
├── start_frontend.bat      # 前端启动脚本(Windows)
└── README_WEB.md          # 说明文档
```

## 功能特性

### 核心功能
- ✅ **多地域支持**: 支持查询阿里云所有地域的抢占式实例价格
- ✅ **多规格对比**: 支持同时查询多个实例规格的价格趋势
- ✅ **灵活筛选**: 支持按可用区、网络类型、操作系统等条件筛选
- ✅ **时间范围**: 支持自定义查询时间范围
- ✅ **实时查询**: 基于FastAPI的高性能API服务
- ✅ **数据导出**: 支持将查询结果导出为CSV格式

### 用户体验
- ✅ **现代化界面**: 基于Element Plus的美观界面
- ✅ **响应式设计**: 支持不同屏幕尺寸
- ✅ **实时反馈**: 查询状态和错误提示
- ✅ **API文档**: 自动生成的Swagger文档

### 技术特性
- ✅ **前后端分离**: 清晰的架构分离
- ✅ **RESTful API**: 标准的REST接口设计
- ✅ **数据验证**: 完善的请求参数验证
- ✅ **错误处理**: 统一的错误处理机制
- ✅ **CORS支持**: 跨域请求支持

## 开发说明

### 后端开发
1. 修改 `backend/config.py` 配置
2. 在 `backend/models.py` 中定义数据模型
3. 在 `backend/main.py` 中添加新的API接口
4. 在 `backend/aliyun_api.py` 中添加新的API调用方法

### 前端开发
1. 在 `frontend/src/views/` 中添加新页面
2. 在 `frontend/src/api/` 中添加新的API调用
3. 在 `frontend/src/router/` 中配置路由
4. 使用Element Plus组件构建界面

### 部署说明
1. **后端部署**: 使用uvicorn或gunicorn部署FastAPI应用
2. **前端部署**: 运行 `npm run build` 构建生产版本
3. **反向代理**: 配置Nginx等反向代理服务器

## 常见问题

### Q: 如何获取阿里云API密钥？
A: 
1. 登录阿里云控制台
2. 点击右上角头像
3. 选择"AccessKey管理"
4. 创建AccessKey和AccessSecret

### Q: 前端无法连接后端怎么办？
A: 
1. 确认后端服务是否启动在8000端口
2. 检查 `frontend/vite.config.js` 中的代理配置
3. 确认CORS配置是否正确

### Q: 查询没有数据怎么办？
A: 
1. 检查API密钥是否正确配置
2. 确认选择的可用区有抢占式实例
3. 尝试不同的时间范围
4. 检查网络连接

## 更新日志
- v1.0.0: 初始Web版本，支持基本的查询和界面功能
- v1.1.0: 添加前后端分离架构和现代化界面
- v1.2.0: 完善API接口和错误处理机制 
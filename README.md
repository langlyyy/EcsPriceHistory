# 阿里云抢占式实例历史价格查询工具

## 项目简介
这是一个用于查询阿里云抢占式实例历史价格的工具，提供现代化的Web界面，支持多规格对比和价格趋势分析。

## 主要功能
1. **地域和可用区选择** - 支持选择不同的地域和可用区
2. **实例规格筛选** - 支持选择不同的实例规格进行查询
3. **网络类型筛选** - 支持Classic和VPC网络类型
4. **时间范围选择** - 支持自定义查询时间范围
5. **多规格对比** - 支持同时查询多个实例规格的价格趋势
6. **价格趋势图表** - 以现代化曲线图形式展示价格变化趋势
7. **数据统计面板** - 实时显示数据点数量、最低价格、最高价格、平均价格
8. **数据导出** - 支持将查询结果导出为CSV格式
9. **响应式设计** - 支持桌面端和移动端访问
10. **现代化UI** - 采用渐变背景、毛玻璃效果、动画交互等现代设计元素

## 版本说明

### Web版本 (前后端分离) ⭐ 主要版本
- 基于FastAPI + Vue.js的现代化Web应用
- 后端: `backend/` 目录
- 前端: `frontend/` 目录
- 运行: `start_web.bat` 或参考 `README_WEB.md`

#### 最新更新 (v2.0)
- ✨ **现代化UI设计**: 采用渐变背景、毛玻璃效果、阴影和动画
- 📊 **数据统计面板**: 实时显示价格统计信息，支持多规格对比统计
- 📱 **响应式设计**: 完美适配桌面端和移动端
- 🎨 **图表优化**: 改进的ECharts配置，支持面积图和渐变效果
- 🔍 **多规格对比**: 支持同时显示多个实例规格的价格趋势曲线
- ⚡ **性能优化**: 优化图表渲染和数据处理
- 🎯 **用户体验**: 添加加载动画、悬停效果和交互反馈
- 🎨 **界面布局优化**: 查询条件模块更紧凑，图表区域占据更多空间
- 📐 **布局比例调整**: 6:18的黄金比例布局，确保图表显示效果最佳

## 安装和使用

### 环境要求
- Python 3.7+
- Node.js 16+
- 阿里云账号和API密钥

### 部署方式

#### 🐳 Docker 部署（推荐）

**系统要求：**
- Docker 20.10+
- Docker Compose 2.0+

**快速部署：**

1. **配置阿里云API密钥：**
   ```bash
   # 编辑配置文件
   vim backend/config.py
   ```
   
   填入你的阿里云AccessKey和AccessSecret：
   ```python
   ALIYUN_ACCESS_KEY_ID = "your_access_key_id"
   ALIYUN_ACCESS_KEY_SECRET = "your_access_key_secret"
   ```

2. **一键部署：**
   ```bash
   # Linux/Mac
   chmod +x deploy.sh
   ./deploy.sh
   
   # Windows
   deploy.bat
   ```

3. **访问应用：**
   - 前端: http://localhost
   - 后端API: http://localhost:8000
   - API文档: http://localhost:8000/docs

**详细说明：** 参考 [Docker部署指南](README_DOCKER.md)

#### 🚀 本地开发部署

**方法一：一键启动（推荐）**
```bash
# Windows用户
start_web.bat

# Linux/Mac用户
./start_web.sh
```

**方法二：分别启动**
1. 启动后端服务：
   ```bash
   start_backend.bat
   ```
   
2. 启动前端服务：
   ```bash
   start_frontend.bat
   ```

**方法三：手动启动**
1. 配置阿里云API密钥：
   - 编辑 `backend/config.py` 文件
   - 填入你的阿里云AccessKey和AccessSecret
   
   **获取API密钥的步骤：**
   - 登录阿里云控制台
   - 点击右上角头像
   - 选择"AccessKey管理"
   - 创建AccessKey和AccessSecret
   - 将密钥信息填入backend/config.py文件

2. 安装后端依赖：
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. 安装前端依赖：
   ```bash
   cd frontend
   npm install
   ```

4. 启动后端服务：
   ```bash
   cd backend
   python main.py
   ```

5. 启动前端服务：
   ```bash
   cd frontend
   npm run dev
   ```

### 使用方法

1. 在浏览器中打开 http://localhost:3000
2. 在界面中选择查询参数：
   - **地域和可用区**: 选择要查询的地域和可用区
   - **实例规格**: 在列表中选择一个或多个实例规格（支持多选）
   - **网络类型**: 选择Classic或VPC网络
   - **操作系统**: 选择Linux或Windows
   - **时间范围**: 设置查询的开始和结束时间

3. 点击"查询价格"按钮获取数据
4. 查看价格趋势图表（支持多规格对比）
5. 可选择"导出数据"保存为CSV文件
6. 使用"清除图表"按钮清空当前显示

### 功能测试

#### Docker部署测试
```bash
# 测试Docker配置
python test_docker.py

# 测试Docker构建
docker-compose build
docker-compose up -d
```

#### 本地开发测试
```bash
# 测试Web应用
python test_web.py
```

测试脚本会检查：
- Docker环境是否正常
- 后端服务是否正常启动
- 前端服务是否正常启动
- API接口是否可用
- 依赖包是否已安装

## 项目结构
```
DescribeSpotPriceHistory/
├── backend/                 # 后端服务 (FastAPI)
│   ├── main.py             # FastAPI主程序
│   ├── models.py           # 数据模型
│   ├── aliyun_api.py       # 阿里云API调用模块
│   ├── config.py           # 配置文件
│   ├── requirements.txt    # Python依赖包
│   ├── Dockerfile          # 后端Docker镜像配置
│   └── .dockerignore       # Docker忽略文件
├── frontend/               # 前端服务 (Vue.js)
│   ├── src/                # 源代码
│   ├── package.json        # Node.js依赖配置
│   ├── vite.config.js      # Vite配置
│   ├── index.html          # 入口HTML
│   ├── Dockerfile          # 前端Docker镜像配置
│   ├── nginx.conf          # Nginx配置文件
│   └── .dockerignore       # Docker忽略文件
├── docker-compose.yml      # Docker Compose配置（开发环境）
├── docker-compose.prod.yml # Docker Compose配置（生产环境）
├── deploy.sh               # Linux/Mac部署脚本
├── deploy.bat              # Windows部署脚本
├── test_docker.py          # Docker配置测试脚本
├── start_web.bat           # 本地开发一键启动脚本
├── start_backend.bat       # 后端启动脚本
├── start_frontend.bat      # 前端启动脚本
├── test_web.py             # Web版本测试脚本
├── README.md               # 项目说明文档
├── README_DOCKER.md        # Docker部署指南
├── README_WEB.md           # Web版本详细文档
└── QUICKSTART_WEB.md       # Web版本快速开始
```

## API参数说明

### DescribeSpotPriceHistory接口参数
- `ZoneId`: 可用区ID（必填）
- `InstanceType`: 实例规格（必填）
- `NetworkType`: 网络类型（classic | vpc）
- `StartTime`: 查询开始时间（yyyy-MM-ddTHH:mm:ssZ格式）
- `EndTime`: 查询结束时间（yyyy-MM-ddTHH:mm:ssZ格式）
- `IoOptimized`: 是否I/O优化（optimized | none）
- `OSType`: 操作系统类型（linux | windows）

### 返回值说明
- `SpotPriceType`: 价格历史记录列表
  - `ZoneId`: 可用区ID
  - `InstanceType`: 实例规格
  - `NetworkType`: 网络类型
  - `SpotPrice`: 价格
  - `Timestamp`: 时间戳

## 注意事项
1. 请确保阿里云API密钥有足够的权限
2. 查询时间范围建议不超过7天，以获得更准确的数据
3. 不同地域的可用区和实例规格可能不同
4. 价格数据可能有延迟，仅供参考

## 功能特点

### 核心功能
- ✅ **多地域支持**: 支持查询阿里云所有地域的抢占式实例价格
- ✅ **多规格对比**: 支持同时查询多个实例规格的价格趋势
- ✅ **灵活筛选**: 支持按可用区、网络类型、操作系统等条件筛选
- ✅ **时间范围**: 支持自定义查询时间范围
- ✅ **图表展示**: 使用ECharts绘制价格趋势曲线图
- ✅ **数据导出**: 支持将查询结果导出为CSV格式

### 用户体验
- ✅ **现代化界面**: 基于Vue.js + Element Plus的现代化Web界面
- ✅ **响应式设计**: 支持桌面和移动设备访问
- ✅ **实时进度**: 显示查询进度和状态信息
- ✅ **错误处理**: 完善的错误提示和处理机制
- ✅ **一键启动**: 提供便捷的启动脚本

### 技术特性
- ✅ **前后端分离**: FastAPI后端 + Vue.js前端
- ✅ **RESTful API**: 标准的REST API设计
- ✅ **数据验证**: 完善的输入参数验证
- ✅ **模块化设计**: 清晰的代码结构和模块分离
- ✅ **配置管理**: 灵活的配置文件系统
- ✅ **依赖管理**: 完整的依赖包管理

## 更新日志
- v1.0.0: 初始版本，支持基本的查询和图表显示功能
- v1.1.0: 添加演示版本、安装脚本和测试功能
- v1.2.0: 完善错误处理和用户体验优化
- v2.0.0: 新增Web版本，前后端分离架构，现代化界面 
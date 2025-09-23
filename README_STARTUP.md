# 🚀 OpenTMP LLM Engine 启动指南

## 📋 项目概述

OpenTMP LLM Engine 是一个综合性的分布式机器学习平台，具有P2P AI智能和Edge AI功能。

## 🏗️ 项目结构

```
webvue/
├── frontend/           # Vue.js 前端应用
│   ├── src/           # 源代码
│   ├── public/        # 静态资源
│   ├── package.json   # 前端依赖
│   └── vite.config.js # Vite 配置
├── backend/           # FastAPI 后端应用
│   ├── main.py        # 主入口文件
│   ├── edgeai/        # Edge AI 模块
│   ├── p2pai/         # P2P AI 模块
│   └── training_service/ # 训练服务
├── database/          # 数据库模块
└── README_STARTUP.md  # 本文件
```

## 🔧 环境要求

### 后端要求
- Python 3.8+
- FastAPI
- Uvicorn

### 前端要求
- Node.js 20.19.0+ 或 22.12.0+
- npm 或 yarn

## 🚀 启动步骤

### 1. 启动后端服务

#### 方法一：使用PYTHONPATH（推荐）
```bash
# 进入项目根目录
cd /home/webvue

# 设置PYTHONPATH并启动后端
PYTHONPATH=/home/webvue python backend/main.py
```

#### 方法二：直接启动（可能遇到模块导入问题）
```bash
# 进入后端目录
cd /home/webvue/backend

# 启动后端服务
python main.py
```

### 2. 启动前端服务

```bash
# 进入前端目录
cd /home/webvue/frontend

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run dev
```

## 📊 服务访问地址

### 后端服务
- **API服务**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **根路径**: http://localhost:8000/

### 前端服务
- **前端界面**: http://localhost:5173
- **Vue DevTools**: http://localhost:5173/__devtools__/

## 🔍 验证服务状态

### 检查后端是否正常运行
```bash
curl http://localhost:8000/health
```
预期响应：
```json
{"status":"healthy"}
```

### 检查前端是否正常运行
```bash
curl http://localhost:5173
```
预期响应：HTML页面内容

### 检查进程状态
```bash
# 查看后端进程
ps aux | grep "python main.py" | grep -v grep

# 查看前端进程
ps aux | grep "vite" | grep -v grep

# 查看端口占用
netstat -tlnp | grep -E ":(8000|5173)"
```

## 🛠️ 常见问题解决

### 1. 后端启动失败 - 模块导入错误

**错误信息**：
```
ModuleNotFoundError: No module named 'database'
```

**解决方案**：
使用PYTHONPATH启动：
```bash
cd /home/webvue
PYTHONPATH=/home/webvue python backend/main.py
```

### 2. 前端端口被占用

**现象**：前端启动时显示端口已被占用

**解决方案**：
```bash
# 停止占用端口的进程
pkill -f "vite"

# 重新启动前端
cd /home/webvue/frontend
npm run dev
```

### 3. 后端端口被占用

**现象**：后端启动时显示端口8000已被占用

**解决方案**：
```bash
# 停止占用端口的进程
pkill -f "python main.py"

# 重新启动后端
cd /home/webvue
PYTHONPATH=/home/webvue python backend/main.py
```

## 📝 开发模式特性

### 后端特性
- ✅ 自动重载：代码修改后自动重启
- ✅ 热重载：实时监控文件变化
- ✅ 详细日志：显示所有API请求

### 前端特性
- ✅ 热重载：代码修改后自动刷新页面
- ✅ Vue DevTools：支持Vue调试工具
- ✅ 快速构建：使用Vite进行快速开发

## 🔄 停止服务

### 停止后端服务
```bash
# 方法1：查找进程ID并终止
ps aux | grep "python main.py" | grep -v grep
kill <进程ID>

# 方法2：直接终止所有相关进程
pkill -f "python main.py"
```

### 停止前端服务
```bash
# 方法1：查找进程ID并终止
ps aux | grep "vite" | grep -v grep
kill <进程ID>

# 方法2：直接终止所有相关进程
pkill -f "vite"
```

## 🎯 API端点说明

### Edge AI API
- `GET /api/edgeai/projects/` - 获取项目列表
- `GET /api/edgeai/nodes/` - 获取节点列表
- `GET /api/edgeai/nodes/visualization/{project_id}/` - 获取可视化数据
- `WebSocket /api/edgeai/nodes/ws/{session_id}` - 实时节点监控

### P2P AI API
- `GET /api/p2pai/nodes/` - 获取P2P节点
- `POST /api/p2pai/training/` - 启动训练任务
- `WebSocket /api/p2pai/training/ws/{session_id}` - 训练进度监控

### 训练服务 API
- `POST /api/training/train` - 启动训练
- `GET /api/training/tasks` - 获取任务列表
- `GET /api/training/health` - 健康检查

## 📚 更多信息

- **项目文档**: 查看项目根目录下的其他README文件
- **API文档**: 访问 http://localhost:8000/docs
- **问题反馈**: 如有问题请检查终端日志输出

## 🎉 快速启动脚本

您也可以创建快速启动脚本：

### 启动脚本 (start.sh)
```bash
#!/bin/bash
echo "🚀 启动 OpenTMP LLM Engine..."

# 启动后端
echo "📡 启动后端服务..."
cd /home/webvue
PYTHONPATH=/home/webvue python backend/main.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端
echo "🌐 启动前端服务..."
cd /home/webvue/frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ 服务启动完成！"
echo "📊 后端API: http://localhost:8000"
echo "🌐 前端界面: http://localhost:5173"
echo "🛑 按 Ctrl+C 停止所有服务"

# 等待用户中断
wait
```

### 停止脚本 (stop.sh)
```bash
#!/bin/bash
echo "🛑 停止所有服务..."
pkill -f "python main.py"
pkill -f "vite"
echo "✅ 所有服务已停止"
```

---

**注意**: 确保在启动服务前已安装所有必要的依赖包。如有问题，请检查终端输出日志。

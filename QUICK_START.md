# ⚡ 快速启动指南

## 🚀 一键启动

### 使用启动脚本（推荐）
```bash
# 启动所有服务
./start.sh

# 停止所有服务
./stop.sh
```

### 手动启动

#### 1. 启动后端
```bash
cd /home/webvue
PYTHONPATH=/home/webvue python backend/main.py
```

#### 2. 启动前端（新终端窗口）
```bash
cd /home/webvue/frontend
npm run dev
```

## 📱 访问地址

- **前端**: http://localhost:5173
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 🛑 停止服务

- **使用脚本**: `./stop.sh`
- **手动停止**: 在终端按 `Ctrl+C`

---

详细说明请查看 `README_STARTUP.md`

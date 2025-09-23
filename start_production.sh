#!/bin/bash

# 生产环境启动脚本
echo "🚀 启动生产环境服务..."

# 设置工作目录
cd /home/webvue

# 启动后端服务 (端口8000)
echo "📡 启动后端API服务..."
cd backend
nohup python main.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"

# 启动前端静态文件服务 (端口3000)
echo "🌐 启动前端静态文件服务..."
cd ../frontend/dist
nohup python -m http.server 3000 > ../../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ 前端服务已启动 (PID: $FRONTEND_PID)"

# 创建日志目录
mkdir -p /home/webvue/logs

# 保存进程ID
echo $BACKEND_PID > /home/webvue/logs/backend.pid
echo $FRONTEND_PID > /home/webvue/logs/frontend.pid

echo "🎉 生产环境服务启动完成！"
echo "📊 后端API: http://localhost:8000"
echo "🌐 前端界面: http://localhost:3000"
echo "📝 日志文件: /home/webvue/logs/"

# 显示服务状态
sleep 2
echo ""
echo "📋 服务状态检查:"
curl -s http://localhost:8000/health > /dev/null && echo "✅ 后端API服务正常" || echo "❌ 后端API服务异常"
curl -s http://localhost:3000 > /dev/null && echo "✅ 前端服务正常" || echo "❌ 前端服务异常"

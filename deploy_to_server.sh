#!/bin/bash

# 服务器部署脚本 - 部署到 175.178.24.56
echo "🚀 开始部署到服务器 175.178.24.56..."

# 设置工作目录
cd /home/webvue

# 创建日志目录
mkdir -p logs

# 1. 检查前端构建文件
echo "📦 检查前端构建文件..."
if [ -d "frontend/dist" ]; then
    echo "✅ 前端构建文件已存在"
else
    echo "⚠️  前端构建文件不存在，跳过构建步骤"
fi

# 2. 启动后端服务 (端口8000)
echo "📡 启动后端API服务..."
cd backend
nohup python main.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"

# 3. 启动前端开发服务器 (端口5173) - 用于服务器部署
echo "🌐 启动前端开发服务器..."
cd ../frontend
nohup npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo "✅ 前端服务已启动 (PID: $FRONTEND_PID)"

# 保存进程ID
echo $BACKEND_PID > /home/webvue/logs/backend.pid
echo $FRONTEND_PID > /home/webvue/logs/frontend.pid

echo "🎉 服务器部署完成！"
echo "📊 后端API: http://175.178.24.56:8000"
echo "🌐 前端界面: http://175.178.24.56:5173"
echo "📝 日志文件: /home/webvue/logs/"

# 等待服务启动
sleep 5

# 显示服务状态
echo ""
echo "📋 服务状态检查:"
curl -s http://175.178.24.56:8000/health > /dev/null && echo "✅ 后端API服务正常" || echo "❌ 后端API服务异常"
curl -s http://175.178.24.56:5173 > /dev/null && echo "✅ 前端服务正常" || echo "❌ 前端服务异常"

echo ""
echo "🔗 访问地址:"
echo "   前端应用: http://175.178.24.56:5173"
echo "   后端API: http://175.178.24.56:8000"
echo "   API文档: http://175.178.24.56:8000/docs"

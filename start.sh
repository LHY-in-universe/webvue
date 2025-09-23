#!/bin/bash

# OpenTMP LLM Engine 快速启动脚本
echo "🚀 启动 OpenTMP LLM Engine..."

# 设置工作目录
cd /home/webvue

# 启动后端服务
echo "📡 启动后端服务..."
PYTHONPATH=/home/webvue python backend/main.py &
BACKEND_PID=$!
echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"

# 等待后端启动
echo "⏳ 等待后端服务启动..."
sleep 5

# 检查后端是否启动成功
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ 后端服务启动成功"
else
    echo "❌ 后端服务启动失败"
    exit 1
fi

# 启动前端服务
echo "🌐 启动前端服务..."
cd /home/webvue/frontend
npm run dev &
FRONTEND_PID=$!
echo "✅ 前端服务已启动 (PID: $FRONTEND_PID)"

# 等待前端启动
echo "⏳ 等待前端服务启动..."
sleep 3

# 检查前端是否启动成功
if curl -s http://localhost:5173 > /dev/null; then
    echo "✅ 前端服务启动成功"
else
    echo "❌ 前端服务启动失败"
    exit 1
fi

echo ""
echo "🎉 所有服务启动完成！"
echo "📊 后端API: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo "🌐 前端界面: http://localhost:5173"
echo "🔧 Vue DevTools: http://localhost:5173/__devtools__/"
echo ""
echo "🛑 按 Ctrl+C 停止所有服务"
echo ""

# 保存进程ID到文件
echo $BACKEND_PID > /tmp/webvue_backend.pid
echo $FRONTEND_PID > /tmp/webvue_frontend.pid

# 等待用户中断
trap 'echo ""; echo "🛑 正在停止服务..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f /tmp/webvue_*.pid; echo "✅ 所有服务已停止"; exit 0' INT

# 保持脚本运行
wait

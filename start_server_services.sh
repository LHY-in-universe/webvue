#!/bin/bash

# 服务器服务启动脚本 - 用于系统重启后自动启动
echo "🚀 启动服务器服务 (175.178.24.56)..."

# 设置工作目录
cd /home/webvue

# 创建日志目录
mkdir -p logs

# 检查服务是否已经在运行
if [ -f logs/backend.pid ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        echo "⚠️  后端服务已在运行 (PID: $BACKEND_PID)"
    else
        echo "🔄 启动后端API服务..."
        cd backend
        nohup python main.py > ../logs/backend.log 2>&1 &
        BACKEND_PID=$!
        echo $BACKEND_PID > ../logs/backend.pid
        echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"
        cd ..
    fi
else
    echo "🔄 启动后端API服务..."
    cd backend
    nohup python main.py > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../logs/backend.pid
    echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"
    cd ..
fi

if [ -f logs/frontend.pid ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        echo "⚠️  前端服务已在运行 (PID: $FRONTEND_PID)"
    else
        echo "🔄 启动前端服务..."
        cd frontend
        nohup npm run dev > ../logs/frontend.log 2>&1 &
        FRONTEND_PID=$!
        echo $FRONTEND_PID > ../logs/frontend.pid
        echo "✅ 前端服务已启动 (PID: $FRONTEND_PID)"
        cd ..
    fi
else
    echo "🔄 启动前端服务..."
    cd frontend
    nohup npm run dev > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../logs/frontend.pid
    echo "✅ 前端服务已启动 (PID: $FRONTEND_PID)"
    cd ..
fi

echo "🎉 服务器服务启动完成！"
echo "📊 后端API: http://175.178.24.56:8000"
echo "🌐 前端界面: http://175.178.24.56:5173"
echo "📝 日志文件: /home/webvue/logs/"

# 等待服务启动
sleep 3

# 显示服务状态
echo ""
echo "📋 服务状态检查:"
curl -s http://175.178.24.56:8000/health > /dev/null && echo "✅ 后端API服务正常" || echo "❌ 后端API服务异常"
curl -s http://175.178.24.56:5173 > /dev/null && echo "✅ 前端服务正常" || echo "❌ 前端服务异常"

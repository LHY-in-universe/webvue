#!/bin/bash

# 服务器服务停止脚本
echo "🛑 停止服务器服务..."

# 设置工作目录
cd /home/webvue

# 停止后端服务
if [ -f logs/backend.pid ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if ps -p $BACKEND_PID > /dev/null 2>&1; then
        kill $BACKEND_PID
        echo "✅ 后端服务已停止 (PID: $BACKEND_PID)"
    else
        echo "⚠️  后端服务未运行"
    fi
    rm -f logs/backend.pid
else
    echo "⚠️  后端服务PID文件不存在"
fi

# 停止前端服务
if [ -f logs/frontend.pid ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null 2>&1; then
        kill $FRONTEND_PID
        echo "✅ 前端服务已停止 (PID: $FRONTEND_PID)"
    else
        echo "⚠️  前端服务未运行"
    fi
    rm -f logs/frontend.pid
else
    echo "⚠️  前端服务PID文件不存在"
fi

# 强制杀死可能残留的进程
pkill -f "python main.py" 2>/dev/null && echo "🧹 清理残留的后端进程"
pkill -f "npm run dev" 2>/dev/null && echo "🧹 清理残留的前端进程"

echo "🎉 所有服务已停止"

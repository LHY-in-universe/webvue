#!/bin/bash

# 生产环境停止脚本
echo "🛑 停止生产环境服务..."

# 停止后端服务
if [ -f /home/webvue/logs/backend.pid ]; then
    BACKEND_PID=$(cat /home/webvue/logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        echo "✅ 后端服务已停止 (PID: $BACKEND_PID)"
    else
        echo "⚠️  后端服务进程不存在"
    fi
    rm -f /home/webvue/logs/backend.pid
else
    echo "⚠️  后端PID文件不存在"
fi

# 停止前端服务
if [ -f /home/webvue/logs/frontend.pid ]; then
    FRONTEND_PID=$(cat /home/webvue/logs/frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        echo "✅ 前端服务已停止 (PID: $FRONTEND_PID)"
    else
        echo "⚠️  前端服务进程不存在"
    fi
    rm -f /home/webvue/logs/frontend.pid
else
    echo "⚠️  前端PID文件不存在"
fi

# 清理可能残留的进程
pkill -f "python main.py" 2>/dev/null
pkill -f "python -m http.server 3000" 2>/dev/null

echo "🎉 生产环境服务已停止"

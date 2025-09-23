#!/bin/bash

# OpenTMP LLM Engine 停止脚本
echo "🛑 停止 OpenTMP LLM Engine 服务..."

# 停止后端服务
echo "📡 停止后端服务..."
if [ -f /tmp/webvue_backend.pid ]; then
    BACKEND_PID=$(cat /tmp/webvue_backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        echo "✅ 后端服务已停止 (PID: $BACKEND_PID)"
    else
        echo "⚠️ 后端服务进程不存在"
    fi
    rm -f /tmp/webvue_backend.pid
else
    echo "⚠️ 未找到后端进程ID文件"
fi

# 停止前端服务
echo "🌐 停止前端服务..."
if [ -f /tmp/webvue_frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/webvue_frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        echo "✅ 前端服务已停止 (PID: $FRONTEND_PID)"
    else
        echo "⚠️ 前端服务进程不存在"
    fi
    rm -f /tmp/webvue_frontend.pid
else
    echo "⚠️ 未找到前端进程ID文件"
fi

# 强制停止所有相关进程（备用方案）
echo "🔍 检查并停止所有相关进程..."
pkill -f "python backend/main.py" 2>/dev/null && echo "✅ 强制停止后端进程"
pkill -f "vite" 2>/dev/null && echo "✅ 强制停止前端进程"

# 检查端口是否释放
echo "🔍 检查端口状态..."
if netstat -tlnp | grep -q ":8000 "; then
    echo "⚠️ 端口8000仍被占用"
else
    echo "✅ 端口8000已释放"
fi

if netstat -tlnp | grep -q ":5173 "; then
    echo "⚠️ 端口5173仍被占用"
else
    echo "✅ 端口5173已释放"
fi

echo ""
echo "🎉 服务停止完成！"

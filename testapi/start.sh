#!/bin/bash

# 启动测试API服务脚本

echo "启动Training Monitor API Mock服务..."

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "安装依赖包..."
pip install -r requirements.txt

# 启动服务
echo "启动API服务在 http://localhost:6677"
echo "API文档地址: http://localhost:6677/docs"
echo "按 Ctrl+C 停止服务"

python main.py

#!/bin/bash

# OpenTMP LLM Engine 依赖安装脚本
# 自动安装前端和后端依赖

set -e  # 遇到错误立即退出

echo "🚀 OpenTMP LLM Engine 依赖安装开始..."
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查 Python
echo "📦 检查 Python..."
if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 未安装，请先安装 Python 3.9+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✅ Python 版本: $PYTHON_VERSION${NC}"

# 检查 pip
if ! command_exists pip3; then
    echo -e "${RED}❌ pip3 未安装${NC}"
    exit 1
fi
echo -e "${GREEN}✅ pip3 已安装${NC}"

# 检查 Node.js
echo ""
echo "📦 检查 Node.js..."
if ! command_exists node; then
    echo -e "${RED}❌ Node.js 未安装，请先安装 Node.js 20.19+${NC}"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✅ Node.js 版本: $NODE_VERSION${NC}"

# 检查包管理器
PACKAGE_MANAGER=""
if command_exists pnpm; then
    PACKAGE_MANAGER="pnpm"
    echo -e "${GREEN}✅ 使用 pnpm 作为包管理器${NC}"
elif command_exists npm; then
    PACKAGE_MANAGER="npm"
    echo -e "${YELLOW}⚠️  使用 npm 作为包管理器 (推荐安装 pnpm)${NC}"
else
    echo -e "${RED}❌ 未找到 npm 或 pnpm${NC}"
    exit 1
fi

# 询问安装类型
echo ""
echo "请选择安装类型："
echo "1) 完整安装 (包含所有依赖)"
echo "2) 最小化安装 (仅核心依赖，快速启动)"
echo "3) 开发环境安装 (包含开发工具)"
read -p "请输入选择 (1/2/3): " INSTALL_TYPE

# 安装后端依赖
echo ""
echo "📦 安装后端依赖..."
cd backend

case $INSTALL_TYPE in
    1)
        echo "安装完整依赖..."
        pip3 install -r requirements.txt
        ;;
    2)
        echo "安装最小化依赖..."
        pip3 install -r requirements-minimal.txt
        ;;
    3)
        echo "安装开发环境依赖..."
        pip3 install -r requirements-dev.txt
        ;;
    *)
        echo -e "${RED}❌ 无效选择，默认安装完整依赖${NC}"
        pip3 install -r requirements.txt
        ;;
esac

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 后端依赖安装成功${NC}"
else
    echo -e "${RED}❌ 后端依赖安装失败${NC}"
    exit 1
fi

# 安装前端依赖
echo ""
echo "📦 安装前端依赖..."
cd ../frontend

if [ "$PACKAGE_MANAGER" = "pnpm" ]; then
    pnpm install
else
    npm install
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 前端依赖安装成功${NC}"
else
    echo -e "${RED}❌ 前端依赖安装失败${NC}"
    exit 1
fi

# 返回根目录
cd ..

echo ""
echo "🎉 依赖安装完成！"
echo ""
echo "📋 后续步骤："
echo "1. 配置环境变量: cp backend/.env.example backend/.env"
echo "2. 启动服务: ./start_server_services.sh"
echo "3. 访问前端: http://175.178.24.56:5173"
echo "4. 访问后端API文档: http://175.178.24.56:8000/docs"
echo ""
echo "📚 更多信息请查看 DEPENDENCIES.md"

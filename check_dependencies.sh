#!/bin/bash

# 依赖检查脚本
# 检查项目所需的所有依赖是否已正确安装

echo "🔍 检查项目依赖..."
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 检查计数
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0

# 检查函数
check_command() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if command -v "$1" >/dev/null 2>&1; then
        VERSION=$($1 --version 2>&1 | head -n 1)
        echo -e "${GREEN}✅ $1: $VERSION${NC}"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        echo -e "${RED}❌ $1: 未安装${NC}"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# 检查Python模块
check_python_module() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if python3 -c "import $1" 2>/dev/null; then
        VERSION=$(python3 -c "import $1; print(getattr($1, '__version__', 'unknown'))" 2>/dev/null)
        echo -e "${GREEN}✅ Python $1: $VERSION${NC}"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        echo -e "${RED}❌ Python $1: 未安装${NC}"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# 检查Node.js包
check_node_package() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    if [ -d "frontend/node_modules/$1" ]; then
        echo -e "${GREEN}✅ Node $1: 已安装${NC}"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        echo -e "${RED}❌ Node $1: 未安装${NC}"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# 系统依赖检查
echo "📦 系统依赖检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_command python3
check_command pip3
check_command node
check_command npm
command -v pnpm >/dev/null 2>&1 && check_command pnpm || echo -e "${YELLOW}⚠️  pnpm: 未安装 (可选，但推荐)${NC}"
check_command git

echo ""
echo "📦 Python后端依赖检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
check_python_module fastapi
check_python_module uvicorn
check_python_module pydantic
check_python_module websockets
check_python_module sqlalchemy
check_python_module psutil

echo ""
echo "📦 Node.js前端依赖检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d "frontend/node_modules" ]; then
    check_node_package vue
    check_node_package vue-router
    check_node_package pinia
    check_node_package tailwindcss
    check_node_package axios
    check_node_package vite
else
    echo -e "${RED}❌ frontend/node_modules 目录不存在${NC}"
    echo -e "${YELLOW}请运行: cd frontend && npm install${NC}"
    FAILED_CHECKS=$((FAILED_CHECKS + 6))
    TOTAL_CHECKS=$((TOTAL_CHECKS + 6))
fi

echo ""
echo "📦 服务状态检查"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查后端服务
if curl -s http://175.178.24.56:8000 >/dev/null 2>&1; then
    echo -e "${GREEN}✅ 后端API服务: 运行中${NC}"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    echo -e "${YELLOW}⚠️  后端API服务: 未运行${NC}"
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

# 检查前端服务
if curl -s http://175.178.24.56:5173 >/dev/null 2>&1; then
    echo -e "${GREEN}✅ 前端服务: 运行中${NC}"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
else
    echo -e "${YELLOW}⚠️  前端服务: 未运行${NC}"
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

echo ""
echo "📊 检查结果摘要"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "总检查项: $TOTAL_CHECKS"
echo -e "${GREEN}通过: $PASSED_CHECKS${NC}"
echo -e "${RED}失败: $FAILED_CHECKS${NC}"

if [ $FAILED_CHECKS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 所有依赖检查通过！${NC}"
    exit 0
else
    echo ""
    echo -e "${YELLOW}⚠️  部分依赖缺失，请运行以下命令安装：${NC}"
    echo ""
    echo "安装所有依赖:"
    echo "  ./install_dependencies.sh"
    echo ""
    echo "或手动安装:"
    echo "  后端: cd backend && pip3 install -r requirements.txt"
    echo "  前端: cd frontend && npm install"
    exit 1
fi


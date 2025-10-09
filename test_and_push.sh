#!/bin/bash

# GitHub SSH 测试和推送脚本

echo "════════════════════════════════════════════════════════════════"
echo "           GitHub SSH 连接测试和代码推送"
echo "════════════════════════════════════════════════════════════════"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. 测试SSH连接
echo "📡 步骤 1: 测试GitHub SSH连接..."
echo ""

SSH_TEST=$(ssh -T git@github.com 2>&1)

if echo "$SSH_TEST" | grep -q "successfully authenticated"; then
    echo -e "${GREEN}✅ SSH连接成功！${NC}"
    echo "$SSH_TEST"
    echo ""
    
    # 2. 推送代码
    echo "════════════════════════════════════════════════════════════════"
    echo "📤 步骤 2: 推送代码到GitHub..."
    echo ""
    
    cd /home/webvue
    
    # 显示提交信息
    echo "提交信息:"
    git log -1 --oneline
    echo ""
    
    # 强制推送
    echo "正在强制推送到 origin/bench..."
    if git push -f origin bench; then
        echo ""
        echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}          🎉 代码推送成功！${NC}"
        echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo "查看提交:"
        echo "https://github.com/LHY-in-universe/webvue/tree/bench"
        echo ""
    else
        echo ""
        echo -e "${RED}❌ 推送失败${NC}"
        exit 1
    fi
    
else
    echo -e "${RED}❌ SSH连接失败${NC}"
    echo ""
    echo "错误信息:"
    echo "$SSH_TEST"
    echo ""
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}⚠️  请按以下步骤配置SSH密钥:${NC}"
    echo -e "${YELLOW}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "1. 复制SSH公钥:"
    echo ""
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "2. 访问 GitHub SSH 设置页面:"
    echo "   https://github.com/settings/keys"
    echo ""
    echo "3. 点击 'New SSH key' 并添加上面的公钥"
    echo ""
    echo "4. 添加后重新运行此脚本:"
    echo "   ./test_and_push.sh"
    echo ""
    exit 1
fi


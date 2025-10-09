================================================================================
                   依赖文件使用说明
================================================================================

本项目包含多个依赖管理文件，本文档说明每个文件的用途和使用方法。

================================================================================
                   📋 依赖文件清单
================================================================================

后端依赖 (Python):
┌─────────────────────────────────────────────────────────────────────┐
│ requirements.txt             完整生产依赖，包含所有功能             │
│ requirements-minimal.txt     最小化依赖，仅核心功能                 │
│ requirements-dev.txt         开发环境依赖，包含测试和调试工具       │
└─────────────────────────────────────────────────────────────────────┘

前端依赖 (Node.js):
┌─────────────────────────────────────────────────────────────────────┐
│ package.json                 NPM配置文件，包含所有前端依赖          │
│ package-lock.json            NPM锁定文件（自动生成）                │
│ DEPENDENCIES.txt             前端依赖说明文档                       │
└─────────────────────────────────────────────────────────────────────┘

文档和脚本:
┌─────────────────────────────────────────────────────────────────────┐
│ DEPENDENCIES.md              完整依赖文档（Markdown格式）           │
│ DEPENDENCIES_SUMMARY.txt     依赖概览（纯文本格式）                │
│ DEPENDENCIES_README.txt      依赖文件使用说明（本文件）            │
│ install_dependencies.sh      依赖安装脚本                          │
│ check_dependencies.sh        依赖检查脚本                          │
└─────────────────────────────────────────────────────────────────────┘

================================================================================
                   🚀 快速开始
================================================================================

方式一：使用自动化脚本（推荐）
-------------------------------
1. 运行安装脚本:
   ./install_dependencies.sh
   
2. 按提示选择安装类型:
   - 选项 1: 完整安装
   - 选项 2: 最小化安装
   - 选项 3: 开发环境安装

方式二：手动安装
-----------------
后端:
  cd backend
  pip install -r requirements.txt

前端:
  cd frontend
  npm install
  # 或使用pnpm
  pnpm install

================================================================================
                   📦 依赖文件详解
================================================================================

1️⃣  requirements.txt (后端完整依赖)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
用途: 
  - 生产环境部署
  - 包含所有功能所需的依赖
  - 包括机器学习、数据处理、Web框架等

包含内容:
  - Web框架: FastAPI, Uvicorn
  - 认证安全: python-jose, passlib
  - 数据库: SQLAlchemy, Alembic
  - 机器学习: PyTorch, Transformers
  - 工具库: pandas, numpy, psutil

何时使用:
  ✅ 部署到生产环境
  ✅ 需要使用所有功能
  ✅ 进行机器学习训练

安装命令:
  pip install -r backend/requirements.txt

2️⃣  requirements-minimal.txt (后端最小依赖)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
用途:
  - 快速启动和测试
  - 仅包含核心Web服务功能
  - 不包含机器学习依赖

包含内容:
  - FastAPI, Uvicorn, Pydantic
  - WebSocket, SQLAlchemy
  - psutil, python-dotenv

何时使用:
  ✅ 快速测试API功能
  ✅ 不需要机器学习功能
  ✅ 资源受限的环境

安装命令:
  pip install -r backend/requirements-minimal.txt

3️⃣  requirements-dev.txt (后端开发环境)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
用途:
  - 开发环境使用
  - 包含所有生产依赖
  - 额外包含开发工具

包含内容:
  - 所有生产依赖 (通过-r requirements.txt引入)
  - 代码格式化: black, isort, autopep8
  - 代码检查: pylint, flake8, mypy
  - 测试框架: pytest, pytest-cov
  - 调试工具: ipython, ipdb

何时使用:
  ✅ 本地开发
  ✅ 编写和运行测试
  ✅ 代码质量检查

安装命令:
  pip install -r backend/requirements-dev.txt

4️⃣  package.json (前端依赖)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
用途:
  - 前端项目配置
  - 管理所有Node.js依赖
  - 定义npm脚本命令

包含内容:
  dependencies (运行时依赖):
    - Vue 3 生态系统
    - UI框架 (Tailwind CSS)
    - 工具库 (axios, chart.js)
  
  devDependencies (开发依赖):
    - 构建工具 (Vite)
    - CSS处理 (PostCSS)
    - 代码优化 (Terser)

何时使用:
  ✅ 前端开发和部署
  ✅ 任何需要运行前端的场景

安装命令:
  cd frontend
  npm install    # 或 pnpm install

================================================================================
                   🔍 依赖检查
================================================================================

使用检查脚本:
--------------
./check_dependencies.sh

脚本会检查:
  ✅ 系统依赖 (Python, Node.js, npm, git)
  ✅ Python包是否正确安装
  ✅ Node.js包是否正确安装
  ✅ 服务运行状态

手动检查:
----------
Python依赖:
  pip list
  pip show fastapi

Node.js依赖:
  npm list
  npm ls vue

================================================================================
                   ⚙️ 依赖更新
================================================================================

更新后端依赖:
-------------
1. 更新所有包:
   pip install --upgrade -r backend/requirements.txt

2. 更新单个包:
   pip install --upgrade fastapi

3. 生成新的requirements:
   pip freeze > backend/requirements-new.txt

更新前端依赖:
-------------
1. 检查过时包:
   npm outdated
   # 或
   pnpm outdated

2. 更新所有包:
   npm update
   # 或
   pnpm update

3. 更新单个包:
   npm install vue@latest
   # 或
   pnpm update vue

================================================================================
                   🐛 常见问题
================================================================================

Q: pip install失败，提示权限错误
A: 使用虚拟环境或添加 --user 参数
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

Q: npm install很慢
A: 使用pnpm或配置淘宝镜像
   npm install -g pnpm
   pnpm install
   
   或配置镜像:
   npm config set registry https://registry.npmmirror.com

Q: 依赖版本冲突
A: 检查冲突并手动解决
   pip check              # Python
   npm ls                 # Node.js

Q: 如何清理依赖
A: 删除并重新安装
   Python:
     pip uninstall -r requirements.txt -y
     rm -rf __pycache__
   
   Node.js:
     rm -rf node_modules package-lock.json
     npm install

Q: 如何添加新依赖
A: 安装后更新requirements文件
   pip install new-package
   pip freeze > requirements.txt

================================================================================
                   📚 相关文档
================================================================================

详细文档:
  - DEPENDENCIES.md             # 完整依赖文档
  - DEPENDENCIES_SUMMARY.txt    # 依赖概览
  - README.md                   # 项目说明

官方文档:
  - FastAPI:      https://fastapi.tiangolo.com/
  - Vue.js:       https://vuejs.org/
  - Vite:         https://vitejs.dev/
  - PyTorch:      https://pytorch.org/
  - Transformers: https://huggingface.co/docs/transformers/

================================================================================
                   💡 最佳实践
================================================================================

1. 使用虚拟环境
   - Python: 使用venv或conda
   - Node.js: 使用nvm管理版本

2. 锁定依赖版本
   - Python: 使用pip freeze
   - Node.js: 提交package-lock.json

3. 定期更新依赖
   - 关注安全更新
   - 测试兼容性

4. 分离开发和生产依赖
   - 减小部署包大小
   - 提高安全性

5. 文档化依赖原因
   - 记录为什么需要某个包
   - 方便后续维护

================================================================================


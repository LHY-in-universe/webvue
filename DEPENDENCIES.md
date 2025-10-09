# OpenTMP LLM Engine 项目依赖文档

## 📋 概述

本文档列出了 OpenTMP LLM Engine 项目的所有依赖项，包括前端和后端。

---

## 🖥️ 后端依赖 (Python)

### Python 版本要求
- Python 3.9+

### 依赖文件
- `backend/requirements.txt` - 完整生产依赖
- `backend/requirements-minimal.txt` - 最小化依赖（快速启动）
- `backend/requirements-dev.txt` - 开发环境依赖

### 核心依赖

#### Web 框架
```
fastapi==0.104.1              # 现代高性能Web框架
uvicorn[standard]==0.24.0     # ASGI服务器
pydantic==2.5.0               # 数据验证
websockets==12.0              # WebSocket支持
```

#### 认证和安全
```
python-jose[cryptography]==3.3.0  # JWT令牌处理
passlib[bcrypt]==1.7.4            # 密码哈希
email-validator==2.1.0            # 邮箱验证
```

#### 数据库
```
sqlalchemy==2.0.23            # ORM框架
alembic==1.13.1               # 数据库迁移工具
```

#### 缓存和消息队列
```
redis==5.0.1                  # Redis客户端
celery==5.3.4                 # 异步任务队列
```

#### 机器学习和数据处理
```
torch==2.1.1                  # PyTorch深度学习框架
transformers==4.36.0          # Hugging Face Transformers
pandas==2.1.4                 # 数据分析
numpy==1.25.2                 # 数值计算
scikit-learn==1.3.2           # 机器学习工具
```

#### 工具库
```
aiofiles==23.2.1              # 异步文件操作
httpx==0.25.2                 # 异步HTTP客户端
psutil==5.9.6                 # 系统监控
python-dotenv==1.0.0          # 环境变量管理
```

### 安装命令

#### 完整安装
```bash
cd backend
pip install -r requirements.txt
```

#### 最小化安装（快速启动）
```bash
cd backend
pip install -r requirements-minimal.txt
```

#### 开发环境安装
```bash
cd backend
pip install -r requirements-dev.txt
```

---

## 🎨 前端依赖 (Node.js)

### Node.js 版本要求
- Node.js ^20.19.0 或 >=22.12.0
- npm 或 pnpm (推荐)

### 依赖文件
- `frontend/package.json` - NPM依赖配置
- `frontend/DEPENDENCIES.txt` - 依赖说明

### 核心依赖

#### Vue.js 生态系统
```json
"vue": "^3.5.18"              // Vue 3 核心框架
"vue-router": "^4.5.1"        // 路由管理
"pinia": "^3.0.3"             // 状态管理
"vue-i18n": "^9.14.5"         // 国际化
```

#### UI 框架
```json
"tailwindcss": "^3.4.17"      // CSS框架
"@tailwindcss/forms": "^0.5.10"  // 表单插件
"@heroicons/vue": "^2.2.0"    // 图标库
```

#### 工具库
```json
"@vueuse/core": "^13.9.0"     // Vue组合式API工具
"axios": "^1.11.0"            // HTTP客户端
"chart.js": "^4.5.0"          // 图表库
```

#### 构建工具
```json
"vite": "^7.0.6"              // 构建工具
"@vitejs/plugin-vue": "^6.0.1"  // Vite Vue插件
"terser": "^5.44.0"           // JS压缩
```

### 安装命令

#### 使用 npm
```bash
cd frontend
npm install
```

#### 使用 pnpm (推荐)
```bash
cd frontend
pnpm install
```

---

## 🚀 快速开始

### 1. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2. 安装前端依赖
```bash
cd frontend
npm install
# 或
pnpm install
```

### 3. 启动服务
```bash
# 在项目根目录
./start_server_services.sh
```

---

## 📦 系统依赖

### 操作系统
- Linux (推荐 Ubuntu 20.04+)
- macOS 10.15+
- Windows 10+ (WSL2 推荐)

### 其他依赖
```
- Python 3.9+
- Node.js 20.19+ 或 22.12+
- PostgreSQL 13+ (可选，用于生产环境)
- Redis 6+ (可选，用于缓存)
- Git 2.25+
```

---

## 🔧 开发工具 (可选)

### Python 开发工具
```
black                  # 代码格式化
pylint                 # 代码检查
pytest                 # 测试框架
ipython                # 交互式Python
```

### Node.js 开发工具
```
eslint                 # 代码检查
prettier               # 代码格式化
@vue/devtools          # Vue开发工具
```

---

## 📝 注意事项

1. **虚拟环境**: 推荐使用 Python 虚拟环境 (venv/conda)
2. **Node版本管理**: 推荐使用 nvm 管理 Node.js 版本
3. **包管理器**: 前端推荐使用 pnpm，速度更快
4. **GPU支持**: 如需GPU加速，请安装对应的 CUDA 版本的 PyTorch

---

## 🆘 常见问题

### Q: 如何更新依赖？
```bash
# Python
pip install --upgrade -r requirements.txt

# Node.js
npm update
# 或
pnpm update
```

### Q: 如何检查依赖冲突？
```bash
# Python
pip check

# Node.js
npm ls
# 或
pnpm why <package-name>
```

### Q: 如何清理依赖？
```bash
# Python
pip uninstall -r requirements.txt -y
rm -rf __pycache__

# Node.js
rm -rf node_modules package-lock.json
npm install
```

---

## 📄 许可证

详见项目根目录的 LICENSE 文件。

---

## 📧 联系方式

如有问题，请提交 Issue 或联系项目维护者。


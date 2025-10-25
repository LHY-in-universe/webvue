# 数据库配置说明

本项目使用PostgreSQL作为主要数据库。

## 快速开始

### 1. 安装PostgreSQL

#### macOS
```bash
brew install postgresql
brew services start postgresql
```

#### Ubuntu/Debian
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 2. 创建数据库

```bash
# 连接到PostgreSQL
sudo -u postgres psql

# 创建数据库
CREATE DATABASE backend;

# 退出
\q
```

### 3. 配置环境变量（可选）

如果需要自定义数据库连接，可以设置环境变量：

```bash
export EDGEAI_DATABASE_URL="postgresql://postgres:12345678@localhost:5432/backend"
```

### 4. 运行数据库迁移

```bash
# 创建初始迁移
alembic revision --autogenerate -m "Initial migration"

# 运行迁移
alembic upgrade head
```

## 默认配置

- **数据库**: backend
- **用户**: postgres
- **密码**: 12345678
- **主机**: localhost
- **端口**: 5432

## 开发环境

开发环境可以继续使用SQLite，设置环境变量：

```bash
export EDGEAI_DATABASE_URL="sqlite:///./database/edgeai/edgeai.db"
```

## 故障排除

### 连接失败
1. 检查PostgreSQL服务是否运行
2. 验证数据库是否存在
3. 检查用户名和密码是否正确

### 权限问题
确保postgres用户有足够的权限访问数据库。

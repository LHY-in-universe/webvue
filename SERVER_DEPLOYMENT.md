# 服务器部署说明

## 部署地址
- **服务器IP**: 175.178.24.56
- **前端应用**: http://175.178.24.56:5173
- **后端API**: http://175.178.24.56:8000
- **API文档**: http://175.178.24.56:8000/docs

## 部署步骤

### 1. 首次部署
```bash
# 运行部署脚本
./deploy_to_server.sh
```

### 2. 启动服务
```bash
# 启动所有服务
./start_server_services.sh
```

### 3. 停止服务
```bash
# 停止所有服务
./stop_server_services.sh
```

### 4. 设置开机自启动（可选）
```bash
# 复制服务文件到系统目录
sudo cp webvue.service /etc/systemd/system/

# 重新加载systemd配置
sudo systemctl daemon-reload

# 启用服务
sudo systemctl enable webvue.service

# 启动服务
sudo systemctl start webvue.service

# 查看服务状态
sudo systemctl status webvue.service
```

## 服务管理

### 查看服务状态
```bash
# 查看进程
ps aux | grep -E "(python main.py|npm run dev)"

# 查看日志
tail -f logs/backend.log
tail -f logs/frontend.log
```

### 重启服务
```bash
# 停止服务
./stop_server_services.sh

# 启动服务
./start_server_services.sh
```

## 配置文件说明

### 前端配置 (vite.config.js)
- 开发服务器绑定到 0.0.0.0:5173
- HMR配置使用服务器IP地址
- API代理配置指向后端服务

### 后端配置 (main.py)
- FastAPI服务绑定到 0.0.0.0:8000
- CORS配置允许前端域名访问
- 信任主机配置包含服务器IP

## 故障排除

### 端口占用检查
```bash
# 检查端口使用情况
netstat -tlnp | grep -E "(5173|8000)"
```

### 防火墙配置
```bash
# 开放端口（如果需要）
sudo ufw allow 5173
sudo ufw allow 8000
```

### 日志查看
```bash
# 实时查看日志
tail -f logs/backend.log logs/frontend.log
```

## 更新部署

当代码有更新时：
```bash
# 停止服务
./stop_server_services.sh

# 拉取最新代码
git pull

# 重新构建前端
cd frontend && npm run build

# 启动服务
cd .. && ./start_server_services.sh
```

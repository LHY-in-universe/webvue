# 🗄️ 节点数据库结构文档

## 概述

本文档描述了为替换硬编码节点数据而设计的完整数据库结构。系统现在完全基于数据库存储，支持动态节点管理和实时数据更新。

## 📊 数据库表结构

### 1. 节点表 (nodes) - 主要表

```sql
CREATE TABLE nodes (
    -- 基础字段
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    project_id INTEGER,
    name VARCHAR(200) NOT NULL,
    
    -- 网络信息
    path_ipv4 VARCHAR(15),                    -- IP地址
    network_latency INTEGER,                  -- 网络延迟(ms)
    
    -- 状态信息
    state VARCHAR(50) DEFAULT 'idle',         -- 节点状态
    node_type VARCHAR(50) DEFAULT 'edge',     -- 节点类型
    role VARCHAR(50) DEFAULT 'worker',        -- 节点角色
    is_active BOOLEAN DEFAULT 1,              -- 是否激活
    
    -- 用户信息
    responsible_user VARCHAR(200),            -- 负责用户
    
    -- 连接信息
    connected_nodes_count INTEGER DEFAULT 0,  -- 连接节点数量
    last_heartbeat DATETIME,                  -- 最后心跳时间
    
    -- 资源使用率
    cpu_usage FLOAT DEFAULT 0.0,              -- CPU使用率
    memory_usage FLOAT DEFAULT 0.0,           -- 内存使用率
    gpu_usage FLOAT DEFAULT 0.0,              -- GPU使用率
    
    -- 硬件信息
    cpu VARCHAR(100),                         -- CPU型号信息
    gpu VARCHAR(100),                         -- GPU型号信息
    memory VARCHAR(50),                       -- 内存容量信息
    hardware_info TEXT,                       -- 硬件详情(JSON)
    
    -- 业务信息
    priority INTEGER DEFAULT 1,               -- 优先级
    location VARCHAR(200),                    -- 位置信息
    specialty VARCHAR(200),                   -- 专业领域
    progress FLOAT DEFAULT 0.0,               -- 训练进度
    uptime FLOAT DEFAULT 0.0,                 -- 运行时间百分比
    
    -- 时间戳
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated_time DATETIME,
    
    -- 外键约束
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(project_id) REFERENCES projects(id)
);
```

### 2. 节点连接表 (node_connections)

```sql
CREATE TABLE node_connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_node_id INTEGER NOT NULL,
    to_node_id INTEGER NOT NULL,
    connection_type VARCHAR(50) DEFAULT 'data',
    strength FLOAT DEFAULT 1.0,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_updated DATETIME,
    is_active BOOLEAN DEFAULT 1,
    
    FOREIGN KEY(from_node_id) REFERENCES nodes(id),
    FOREIGN KEY(to_node_id) REFERENCES nodes(id),
    UNIQUE(from_node_id, to_node_id)
);
```

### 3. 节点性能指标表 (node_metrics)

```sql
CREATE TABLE node_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    node_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    cpu_usage FLOAT,
    memory_usage FLOAT,
    gpu_usage FLOAT,
    network_usage FLOAT,
    temperature FLOAT,
    power_consumption FLOAT,
    disk_usage FLOAT,
    
    FOREIGN KEY(node_id) REFERENCES nodes(id)
);
```

## 🔗 表关系图

```
users (用户表)
├── 1:N → projects (项目表)
├── 1:N → models (模型表)
└── 1:N → nodes (节点表)

projects (项目表)
├── N:1 → users (用户表)
├── 1:N → models (模型表)
└── 1:N → nodes (节点表)

nodes (节点表)
├── N:1 → users (用户表)
├── N:1 → projects (项目表)
├── 1:N → node_connections (连接关系)
└── 1:N → node_metrics (性能指标)
```

## 📋 字段映射表

| 前端表格列 | 数据库字段 | 数据类型 | 说明 |
|------------|------------|----------|------|
| **Node Name** | `nodes.name` | VARCHAR(200) | 节点名称 |
| **Role** | `nodes.role` | VARCHAR(50) | 节点角色 |
| **Status** | `nodes.state` | VARCHAR(50) | 节点状态 |
| **Responsible User** | `nodes.responsible_user` | VARCHAR(200) | 负责用户 |
| **IP Address** | `nodes.path_ipv4` | VARCHAR(15) | IP地址 |
| **Connected Nodes** | `nodes.connected_nodes_count` | INTEGER | 连接节点数 |
| **Training Progress** | `nodes.progress` | FLOAT | 训练进度 |
| **CPU** | `nodes.cpu_usage` | FLOAT | CPU使用率 |
| **Memory** | `nodes.memory_usage` | FLOAT | 内存使用率 |
| **GPU** | `nodes.gpu_usage` | FLOAT | GPU使用率 |
| **Last Heartbeat** | `nodes.last_heartbeat` | DATETIME | 最后心跳时间 |

## 🚀 API端点

### 节点管理
- `GET /api/edgeai/nodes/` - 获取所有节点
- `GET /api/edgeai/nodes/{node_id}` - 获取特定节点
- `GET /api/edgeai/nodes/stats/overview` - 获取节点统计
- `GET /api/edgeai/nodes/visualization/{project_id}/` - 获取可视化数据

### 节点操作
- `POST /api/edgeai/nodes/{node_id}/operation` - 执行节点操作
- `GET /api/edgeai/nodes/{node_id}/metrics` - 获取节点指标

## 📊 当前数据状态

| 表名 | 记录数 | 状态 |
|------|--------|------|
| users | 1 | 系统管理员用户 |
| projects | 1 | 联邦学习项目 |
| nodes | 4 | 示例节点数据 |
| node_connections | 4 | 节点连接关系 |
| node_metrics | 40 | 性能指标历史 |

## 🎯 示例节点数据

### 1. Global Model Server
- **类型**: model
- **角色**: Coordinator
- **状态**: online
- **IP**: 192.168.1.100
- **连接节点**: 12个
- **负责用户**: System Administrator

### 2. Backup Model Server
- **类型**: model
- **角色**: Backup
- **状态**: online
- **IP**: 192.168.1.101
- **连接节点**: 8个
- **负责用户**: System Administrator

### 3. Coordinator Node
- **类型**: control
- **角色**: Coordinator
- **状态**: online
- **IP**: 192.168.1.102
- **连接节点**: 15个
- **负责用户**: Network Admin

### 4. Control Node
- **类型**: control
- **角色**: Participant
- **状态**: online
- **IP**: Unknown
- **连接节点**: 0个
- **负责用户**: System

## ✅ 迁移完成状态

- [x] 数据库表结构设计
- [x] 字段迁移脚本执行
- [x] 示例数据导入
- [x] API代码更新
- [x] 硬编码替换
- [x] 前后端集成测试
- [x] 数据验证完成

## 🔧 维护说明

1. **添加新节点**: 直接插入到 `nodes` 表
2. **更新节点状态**: 修改 `nodes.state` 字段
3. **记录性能指标**: 插入到 `node_metrics` 表
4. **管理连接关系**: 使用 `node_connections` 表

## 📈 性能优化

- 为常用查询字段创建了索引
- 使用外键约束保证数据完整性
- 支持JSON格式存储复杂硬件信息
- 分离历史指标数据到独立表

---

**总结**: 系统已完全从硬编码迁移到数据库驱动，支持动态节点管理和实时数据更新。所有前端表格数据现在都来自数据库，实现了真正的数据持久化存储。






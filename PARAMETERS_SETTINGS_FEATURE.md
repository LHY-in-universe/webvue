# Edge AI 可视化页面参数设置功能

## 功能概述

在 Edge AI 可视化页面 (`http://localhost:5173/edgeai/visualization/1`) 添加了完整的参数设置功能，用户可以通过界面配置联邦学习训练的各种参数。

## 新增功能

### 1. 参数设置按钮
- 在页面顶部导航栏添加了"参数设置"按钮
- 点击按钮可以打开参数设置模态框

### 2. 参数设置模态框
包含以下参数配置项：

#### 训练算法设置
- **训练算法 (training_alg)**: SFT, RLHF, DPO, PPO
- **联邦算法 (fed_alg)**: FedAvg, FedProx, FedNova, SCAFFOLD, FedOpt

#### 安全聚合设置
- **安全聚合 (secure_aggregation)**: Shamir Threshold, Paillier, Secure Aggregation, None
- **计算机数量 (num_computers)**: 1-100

#### 训练配置
- **阈值 (threshold)**: 1 到计算机数量之间
- **训练轮次 (num_rounds)**: 1-1000
- **客户端数量 (num_clients)**: 1-100
- **采样客户端 (sample_clients)**: 1 到客户端数量之间

#### 训练参数
- **最大步数 (max_steps)**: 1-10000
- **学习率 (lr)**: 文本输入，如 "1e-4"

#### 模型和数据集
- **模型路径 (model_name_or_path)**: 如 "sshleifer/tiny-gpt2"
- **数据集名称 (dataset_name)**: 如 "vicgalle/alpaca-gpt4"
- **数据集采样数量 (dataset_sample)**: 1-10000

### 3. 参数管理功能
- **保存设置**: 将参数保存到 localStorage
- **重置默认值**: 恢复为预设的默认参数
- **参数验证**: 自动验证参数之间的逻辑关系
- **持久化存储**: 页面刷新后参数设置仍然保留

### 4. 界面集成
- 参数设置会影响页面顶部的训练配置显示
- 支持深色/浅色主题切换
- 响应式设计，适配不同屏幕尺寸

## 默认参数值

```json
{
  "training_alg": "sft",
  "fed_alg": "fedavg", 
  "secure_aggregation": "shamir_threshold",
  "num_computers": 3,
  "threshold": 2,
  "num_rounds": 10,
  "num_clients": 2,
  "sample_clients": 2,
  "max_steps": 100,
  "lr": "1e-4",
  "model_name_or_path": "sshleifer/tiny-gpt2",
  "dataset_name": "vicgalle/alpaca-gpt4",
  "dataset_sample": 50
}
```

## 使用方法

1. 访问 `http://localhost:5173/edgeai/visualization/1`
2. 点击页面右上角的"参数设置"按钮
3. 在模态框中修改所需的参数
4. 点击"保存设置"按钮保存配置
5. 参数会自动应用到训练配置显示中

## 技术实现

- 使用 Vue 3 Composition API
- 响应式数据绑定
- localStorage 持久化存储
- 表单验证和错误处理
- 模态框组件设计
- 深色主题支持

## 文件修改

主要修改了 `/home/webvue/frontend/src/views/edgeai/Visualization.vue` 文件：
- 添加了参数设置模态框模板
- 添加了参数管理相关的响应式数据
- 实现了参数保存、加载、验证等功能
- 集成了参数设置与训练配置显示

功能已完全实现并可以正常使用！

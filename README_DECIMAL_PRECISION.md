# 数字保留两位小数修复报告

## 修复概述

本次修复确保了整个系统中所有数字数据都严格保留两位小数精度，涉及数据库存储、后端API处理和前端显示三个层面。

## 修复内容

### 1. 数据库模型修复 ✅

**文件**: `database/edgeai/models.py`

**修改内容**:
- 将所有数值字段从 `Float` 类型改为 `DECIMAL` 类型
- `progress`: `Float` → `DECIMAL(5,2)` (0.00-100.00)
- `cpu_usage`, `memory_usage`, `disk_usage`: `Float` → `DECIMAL(5,2)` (0.00-100.00)
- `accuracy`: `Float` → `DECIMAL(5,2)` (0.00-100.00)
- `loss`: `Float` → `DECIMAL(8,2)` (支持更大的损失值)
- `size`: `Float` → `DECIMAL(10,2)` (文件大小，支持GB级别)
- `sent`, `received`: `Float` → `DECIMAL(10,2)` (数据传输量)

### 2. 后端API处理修复 ✅

**文件**: `backend/edgeai/api/training.py`

**修改内容**:
- 在所有数值赋值操作中添加 `round(float(value), 2)`
- 确保从外部API获取的数据在存储前保留两位小数
- 涉及的函数:
  - `sync_nodes_from_testapi()`: 节点数据同步时的数值处理
  - `poll_training_status()`: 训练进度更新时的数值处理
  - `periodic_sync_task()`: 定期同步时的数值处理

### 3. 前端数据预处理 ✅

**新增文件**:
- `frontend/src/utils/numberUtils.js`: 数值处理工具函数
- `frontend/src/composables/useFormValidation.js`: 表单验证组件

**核心功能**:
- `formatToDecimal()`: 格式化数字到指定小数位数
- `formatPercentage()`: 格式化百分比 (0.00-100.00)
- `preprocessFormData()`: 预处理表单数据确保精度
- 完整的数值验证和范围检查

**修改的存储文件**: `frontend/src/stores/edgeai.js`
- 在创建项目和节点时预处理数值数据
- 确保所有数值在发送到后端前都经过格式化

### 4. 数据库迁移脚本 ✅

**新增文件**:
- `database/migrations/001_decimal_precision_migration.sql`: SQL迁移脚本
- `database/migrations/run_migration.py`: Python迁移执行脚本

**功能**:
- 自动备份现有数据
- 安全地将现有Float字段转换为DECIMAL类型
- 添加数值范围约束确保数据完整性
- 支持回滚操作

### 5. 测试验证 ✅

**新增文件**: `tests/test_decimal_precision.py`

**测试覆盖**:
- ✅ 数据库模型类型验证
- ✅ 后端数值舍入逻辑测试
- ✅ 前端工具函数测试
- ✅ 迁移脚本验证
- ✅ API端点测试 (可选)

**测试结果**: 5/5 测试通过 🎉

## 使用指南

### 运行数据库迁移

```bash
# 进入项目根目录
cd /Users/lhy/Desktop/Git/webvue

# 运行迁移脚本
python database/migrations/run_migration.py

# 如需回滚
python database/migrations/run_migration.py rollback
```

### 验证修复效果

```bash
# 运行测试脚本
python tests/test_decimal_precision.py
```

### 前端使用示例

```javascript
import { formatToDecimal, formatPercentage, preprocessFormData } from '@/utils/numberUtils'

// 格式化数值
const progress = formatPercentage(87.456)  // 返回 87.46
const fileSize = formatToDecimal(1024.789, 2)  // 返回 1024.79

// 预处理表单数据
const processedData = preprocessFormData(formData)
```

## 数据精度保证

### 数值范围约束

- **百分比字段** (progress, cpu_usage, memory_usage, disk_usage, accuracy): 0.00 - 100.00
- **文件大小** (size): ≥ 0.00, 最大支持 99999999.99 MB
- **传输量** (sent, received): ≥ 0.00, 最大支持 99999999.99 MB
- **损失值** (loss): ≥ 0.00, 最大支持 999999.99

### 错误处理

- 无效输入自动转换为 0.00
- 超出范围的值自动截取到有效范围内
- 完整的输入验证和用户友好的错误提示

## 影响范围

### 数据库层面
- 所有数值字段现在使用DECIMAL类型存储，确保精确的小数计算
- 不再有浮点数精度丢失问题

### API层面
- 所有数值在处理时都会自动舍入到两位小数
- API响应中的数值保证精度一致性

### 前端层面
- 用户输入的数值会自动格式化
- 显示的数值严格保留两位小数
- 表单验证确保数据完整性

## 注意事项

1. **向后兼容**: 现有的Float字段会通过迁移脚本自动转换，不会丢失数据
2. **性能影响**: DECIMAL类型比Float稍慢，但对于我们的应用场景影响可忽略
3. **精度保证**: 数据库到前端显示的整个链路都确保了精度一致性
4. **备份建议**: 运行迁移前建议手动备份重要数据

## 验证清单

- [x] 数据库模型使用DECIMAL类型
- [x] 后端API正确处理数值精度
- [x] 前端工具函数工作正常
- [x] 数据库迁移脚本可执行
- [x] 所有测试通过
- [x] 数值范围约束生效
- [x] 错误处理机制完善

本次修复全面解决了系统中数字精度不一致的问题，确保了从数据存储到用户界面显示的全链路数值精度统一。
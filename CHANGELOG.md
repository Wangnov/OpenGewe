# OpenGewe 更新日志

本文档记录了 OpenGewe 项目的版本更新历史。

## v0.1.0 (2025-05-23)

### ✨ 新功能

- **🚀 高性能函数序列化支持**
  - 使用 Joblib 替代原有的代码字符串序列化方式
  - 解决了 Celery 消息序列化的兼容性问题
  - 支持 LZ4 压缩，提升序列化性能
  - 完美支持异步和同步函数的跨进程执行

- **📊 消息队列状态监控**
  - 新增 `get_queue_status()` 方法，实时查看队列状态
  - 支持查看活跃任务、预约任务、保留任务数量
  - 显示工作进程数量和已处理消息统计
  - 提供详细的队列健康状态信息

- **🧹 队列管理功能**
  - 新增 `clear_queue()` 方法，支持清空待处理消息
  - 自动取消未完成的 Future 对象
  - 提供准确的清除统计信息

- **⚙️ 增强的 Celery Worker 启动脚本**
  - 支持 `--type` 参数快速切换 Redis/RabbitMQ
  - 完整的命令行参数支持（broker、backend、queue、concurrency、log-level）
  - 智能配置优先级：命令行参数 > 环境变量 > 默认值
  - 自动检测配置变更并重新创建 Celery 应用
  - 丰富的帮助信息和使用示例

### 🔧 改进

- **🛡️ 增强错误处理机制**
  - 改进函数序列化失败的错误提示
  - 优化 Worker 连接失败的诊断信息
  - 增加超时异常的详细说明和解决建议

- **📈 性能优化**
  - 使用临时文件优化大型函数对象的序列化
  - 自动资源清理，避免内存泄漏
  - 优化异步任务的等待机制

- **🔗 客户端配置优化**
  - 为 GeweClient 添加 `callback_url` 和 `download_url` 的默认值
  - 简化客户端初始化流程

### 🐛 修复

- **解决函数序列化缩进问题**
  - 修复了 `IndentationError: unexpected indent` 错误
  - 消除了代码字符串执行的稳定性问题

- **修复 Celery Worker 导入问题**
  - 优化模块导入，避免循环依赖
  - 修复启动脚本的模块引用

### 📦 依赖更新

- **新增依赖**
  - `joblib>=1.5.0` - 高性能函数序列化
  - `lz4>=4.4.4` - 快速压缩支持

- **依赖优化**
  - 更新现有依赖的版本范围
  - 优化 requirements.txt 格式

### 🔧 技术细节

#### 消息队列架构升级

**之前的问题：**
```python
# 旧方式：使用 inspect.getsource() + exec()
source_code = inspect.getsource(func)  # 保留原始缩进
exec(func_code, global_vars, local_vars)  # 导致缩进错误
```

**新的解决方案：**
```python
# 新方式：使用 joblib 序列化
joblib.dump(func, temp_file_path, compress='lz4')
func = joblib.load(temp_file_path)
```

#### Celery Worker 启动方式

**新的启动选项：**
```bash
# 使用 Redis（默认）
python -m opengewe.queue.celery_worker

# 使用 RabbitMQ
python -m opengewe.queue.celery_worker --type rabbitmq

# 自定义配置
python -m opengewe.queue.celery_worker --type redis --concurrency 8 --log-level debug

# 完全自定义
python -m opengewe.queue.celery_worker --broker redis://host:6379/1 --backend redis://host:6379/2
```

### 📝 使用示例

#### 队列状态监控
```python
# 获取队列状态
status = await queue.get_queue_status()
print(f"队列大小: {status['queue_size']}")
print(f"活跃任务: {status['active_tasks']}")
print(f"工作进程: {status['worker_count']}")
```

#### 清空队列
```python
# 清空所有待处理消息
cleared_count = await queue.clear_queue()
print(f"已清除 {cleared_count} 个待处理任务")
```

### ⚠️ 破坏性变更

- **Celery Worker 导入变更**
  - 移除了 `celery_worker.py` 中的直接 celery 导入
  - 现在使用动态创建的 Celery 应用实例

### 🎯 升级指南

1. **更新依赖**
   ```bash
   pip install opengewe==0.1.0
   ```

2. **重启 Celery Worker**
   ```bash
   # 停止旧的 worker
   pkill -f "celery.*worker"
   
   # 使用新的启动方式
   python -m opengewe.queue.celery_worker --type redis
   ```

3. **检查队列状态**
   ```python
   status = await your_queue.get_queue_status()
   print("队列状态:", status)
   ```


## v0.0.6 (2025-05-23)

### 核心架构优化
1. **重构消息模型系统**：完全重构了消息对象架构，添加异步`from_dict`方法支持，优化消息创建和处理逻辑
2. **新增同步消息处理器**：添加`SyncHandler`处理器，提供同步消息处理能力，增强消息处理的灵活性
3. **优化工厂模式**：改进消息工厂类，提升消息对象创建效率和可维护性

### 技术改进
* **代码优化**：通过重构减少约400行代码，同时增强功能性和可读性
* **异步支持增强**：全面提升异步处理能力，优化高并发场景下的性能表现
* **模型统一化**：统一消息模型接口，简化插件开发和维护工作

### 开发者体验
* 简化了消息处理逻辑的实现
* 提供更一致的API接口
* 增强了代码的可维护性和扩展性

## v0.0.5 (2025-05-22)

### 主要更新内容
1. **修复配置读取问题**：正确解析`main_config.toml`中的插件配置路径
2. **优化插件管理**：修复插件系统的错误恢复能力，添加失败重试机制
3. **增强客户端错误处理**：改进API请求中的错误处理逻辑，提供更详细的错误信息
4. **更新视频号API**：修复视频号(finder)模块中的参数不匹配问题
5. **改进群组消息处理**：新增对群成员被移除等场景的消息处理
6. **优化日志系统**：增强日志格式和配置灵活性
7. **更新依赖要求**：明确指定依赖库的版本范围，避免兼容性问题

### 安全性改进
* 修改插件管理器，不再直接修改TOML配置文件，降低潜在的数据损坏风险

### 开发者变更
* 更新了插件开发文档
* 修复了API文档中的不一致问题

## v0.0.4 (2025-05-21)

* 初始公开发布
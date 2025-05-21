# OpenGewe FastAPI 后端服务详细实施计划

## 目录

1. [项目概述](#项目概述)
2. [目录结构](#目录结构)
3. [模块划分](#模块划分)
4. [API端点设计](#API端点设计)
5. [数据库模式](#数据库模式)
6. [配置项规划](#配置项规划)
7. [重构步骤](#重构步骤)
8. [集成策略](#集成策略)
9. [自定义日志实现方案](#自定义日志实现方案)
10. [Redis集成初步方案](#Redis集成初步方案)
11. [任务分解与优先级](#任务分解与优先级)
12. [风险与挑战](#风险与挑战)

## 项目概述

本计划详细描述了开发完整的、模块化的FastAPI后端服务的步骤。本后端服务是一个微信机器人管理后台，将通过调用 `opengewe` 包的功能，在配置好插件的情况下，按照插件的，同时提供更强大的扩展性、可维护性和可测试性。服务将支持MySQL数据持久化，并预留Redis接口以支持多机器人状态管理。

### 项目目标

1. 创建模块化、可扩展的FastAPI后端服务
2. 保持与 `opengewe` 包的松耦合集成
3. 实现数据库支持(MySQL)
4. 预留Redis接口以支持多机器人状态管理
5. 为前端提供更多，更完整的API接口

## 目录结构

```
backend/
│
├── app/                      # 应用主目录
│   ├── __init__.py           # 初始化应用
│   ├── main.py               # 应用入口点
│   ├── api/                  # API路由
│   │   ├── __init__.py
│   │   ├── routes/           # API路由定义
│   │   │   ├── __init__.py
│   │   │   ├── webhook.py    # 回调接口
│   │   │   ├── plugin.py     # 插件管理接口
│   │   │   ├── file.py       # 文件下载接口
│   │   │   ├── robot.py      # 机器人管理接口
│   │   │   ├── system.py     # 系统设置接口
│   │   │   └── admin.py      # 管理接口
│   │   └── deps.py           # 依赖注入
│   │
│   ├── core/                 # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py         # 应用配置
│   │   ├── security.py       # 安全设置
│   │   └── exceptions.py     # 异常处理
│   │
│   ├── db/                   # 数据库相关
│   │   ├── __init__.py
│   │   ├── session.py        # 数据库会话
│   │   ├── base.py           # 基础模型
│   │   └── init_db.py        # 数据库初始化
│   │
│   ├── models/               # 数据库模型
│   │   ├── __init__.py
│   │   ├── plugin.py         # 插件模型
│   │   ├── robot.py          # 机器人模型
│   │   ├── user.py           # 用户模型
│   │   └── config.py         # 配置模型
│   │
│   ├── schemas/              # Pydantic模型
│   │   ├── __init__.py
│   │   ├── plugin.py         # 插件架构
│   │   ├── robot.py          # 机器人架构
│   │   ├── user.py           # 用户架构
│   │   └── config.py         # 配置架构
│   │
│   ├── services/             # 业务逻辑服务
│   │   ├── __init__.py
│   │   ├── plugin_service.py # 插件服务
│   │   ├── robot_service.py  # 机器人服务
│   │   ├── admin_service.py  # 管理服务
│   │   └── file_service.py   # 文件服务
│   │
│   ├── utils/                # 工具函数
│   │   ├── __init__.py
│   │   ├── redis_manager.py  # Redis管理器
│   │   └── logger_config.py  # 日志配置
│   │
│   └── gewe/                 # GeweClient集成
│       ├── __init__.py
│       ├── client_factory.py # 客户端工厂
│       └── client_manager.py # 客户端管理器
│
├── tests/                    # 测试目录
│   ├── __init__.py
│   ├── conftest.py           # 测试配置
│   ├── test_api/             # API测试
│   │   ├── __init__.py
│   │   ├── test_webhook.py
│   │   ├── test_plugin.py
│   │   └── ...
│   └── test_services/        # 服务测试
│       ├── __init__.py
│       ├── test_plugin_service.py
│       └── ...
│
│
├── scripts/                  # 实用脚本
│   ├── create_user.py        # 创建管理用户
│   └── init_db.py            # 初始化数据库
│
└── requirements.txt  # 后端依赖
```

## 模块划分

### 1. API路由模块

职责：处理HTTP请求、输入验证、路由到适当的服务

**主要组件：**
- `routes/webhook.py`: 处理微信回调消息
- `routes/plugin.py`: 管理插件（启用、禁用、配置）
- `routes/file.py`: 处理文件下载请求
- `routes/robot.py`: 管理多个机器人实例
- `routes/system.py`: 系统设置（日志级别等）
- `routes/admin.py`: 管理员操作

### 2. 服务模块

职责：实现业务逻辑，协调数据访问和外部服务

**主要组件：**
- `plugin_service.py`: 插件管理业务逻辑
- `robot_service.py`: 机器人管理业务逻辑
- `admin_service.py`: 管理操作业务逻辑
- `file_service.py`: 文件处理业务逻辑

### 3. 数据库模块

职责：数据库会话管理、模型定义、查询操作

**主要组件：**
- `session.py`: 数据库会话工厂
- `base.py`: 基础模型类
- `init_db.py`: 数据库初始化和迁移

### 4. 模型模块

职责：定义数据库模型

**主要组件：**
- `plugin.py`: 插件信息模型
- `robot.py`: 机器人信息模型
- `user.py`: 用户信息模型
- `config.py`: 配置信息模型

### 5. Schema模块

职责：定义API请求和响应模型

**主要组件：**
- `plugin.py`: 插件相关请求/响应模型
- `robot.py`: 机器人相关请求/响应模型
- `user.py`: 用户相关请求/响应模型
- `config.py`: 配置相关请求/响应模型

### 6. 核心模块

职责：应用配置、安全设置、异常处理

**主要组件：**
- `config.py`: 应用配置管理
- `security.py`: 认证和授权
- `exceptions.py`: 自定义异常和错误处理

### 7. 工具模块

职责：通用工具函数和组件

**主要组件：**
- `redis_manager.py`: Redis连接和操作
- `logger_config.py`: 日志配置和管理

### 8. GeweClient集成模块

职责：管理与opengewe包的集成

**主要组件：**
- `client_factory.py`: 创建GeweClient实例
- `client_manager.py`: 管理多个GeweClient实例

## API端点设计

### 回调API

```
POST /api/webhook
- 处理外部微信的回调消息
- 请求体: 微信回调消息JSON
- 响应: {"status": "success"}
```

### 插件管理API

```
GET /api/plugins
- 获取所有插件列表
- 响应: 插件列表

GET /api/plugins/{plugin_name}
- 获取特定插件详情
- 响应: 插件详情

POST /api/plugins/{plugin_name}/enable
- 启用特定插件
- 响应: {"status": "success", "message": "Plugin enabled"}

POST /api/plugins/{plugin_name}/disable
- 禁用特定插件
- 响应: {"status": "success", "message": "Plugin disabled"}

GET /api/plugins/{plugin_name}/config
- 获取插件配置
- 响应: 插件配置

PUT /api/plugins/{plugin_name}/config
- 更新插件配置
- 请求体: 新的配置数据
- 响应: {"status": "success", "message": "Config updated"}
```

### 文件管理API

```
GET /api/files/{filename}
- 下载文件
- 响应: 文件数据

GET /api/files
- 获取可下载文件列表
- 响应: 文件列表
```

### 机器人管理API

```
GET /api/robots
- 获取所有机器人列表
- 响应: 机器人列表

GET /api/robots/{robot_id}
- 获取特定机器人详情
- 响应: 机器人详情

POST /api/robots
- 创建新机器人实例
- 请求体: 机器人配置
- 响应: 新机器人详情

DELETE /api/robots/{robot_id}
- 删除机器人实例
- 响应: {"status": "success", "message": "Robot deleted"}

GET /api/robots/{robot_id}/status
- 获取机器人状态
- 响应: 机器人状态详情

POST /api/robots/{robot_id}/login
- 触发机器人登录流程
- 响应: {"status": "success", "qrcode_url": "..."}

POST /api/robots/{robot_id}/logout
- 触发机器人登出
- 响应: {"status": "success", "message": "Logged out"}
```

### 系统API

```
GET /api/system/status
- 获取系统状态
- 响应: 系统状态信息

GET /api/system/logs
- 获取系统日志
- 参数: level, page, limit
- 响应: 日志列表

PUT /api/system/log-level
- 设置日志级别
- 请求体: {"level": "INFO"}
- 响应: {"status": "success", "message": "Log level updated"}

GET /api/system/config
- 获取系统配置
- 响应: 系统配置

PUT /api/system/config
- 更新系统配置
- 请求体: 新的配置数据
- 响应: {"status": "success", "message": "Config updated"}
```

### 管理API

```
POST /api/admin/users
- 创建管理用户
- 请求体: 用户信息
- 响应: 新用户信息(不含密码)

GET /api/admin/users
- 获取所有用户
- 响应: 用户列表

PUT /api/admin/users/{user_id}
- 更新用户信息
- 请求体: 用户信息
- 响应: {"status": "success", "message": "User updated"}

DELETE /api/admin/users/{user_id}
- 删除用户
- 响应: {"status": "success", "message": "User deleted"}
```

## 数据库模式

### 插件表 (plugins)

```sql
CREATE TABLE plugins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    directory VARCHAR(255) NOT NULL,
    version VARCHAR(50),
    author VARCHAR(100),
    description TEXT,
    enabled BOOLEAN DEFAULT 0,
    config TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 机器人表 (robots)

```sql
CREATE TABLE robots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    app_id VARCHAR(100) UNIQUE,
    token VARCHAR(100),
    base_url VARCHAR(255) NOT NULL,
    download_url VARCHAR(255),
    callback_url VARCHAR(255),
    status VARCHAR(50) DEFAULT 'offline',
    config TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 用户表 (users)

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    is_admin BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 配置表 (configs)

```sql
CREATE TABLE configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    value TEXT,
    description TEXT,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 配置项规划

main_config.toml 将包含以下关键配置项：

```toml
[backend]
host = "0.0.0.0"          # 后端服务绑定地址
port = 5433               # 后端服务端口
debug = false             # 是否开启调试模式
secret_key = "your-secret-key-here"  # 用于JWT令牌等的密钥
cors_origins = ["*"]      # CORS源
enable_docs = true        # 是否启用OpenAPI文档
docs_url = "/docs"        # API文档URL
enable_redis = false      # 是否启用Redis
enable_admin = true       # 是否启用管理接口

[database]
type = "sqlite"           # 数据库类型: "sqlite" 或 "mysql"
# SQLite配置
sqlite_file = "./backend.db"
# MySQL配置
mysql_user = "username"
mysql_password = "password"
mysql_host = "localhost"
mysql_port = 3306
mysql_database = "opengewe"
connect_args = {}         # 额外连接参数

[redis]
host = "localhost"        # Redis服务器地址
port = 6379               # Redis端口
db = 0                    # Redis数据库索引
password = ""             # Redis密码
prefix = "opengewe:"      # Redis键前缀

[queue]
# 消息队列类型，可选值为"simple"或"advanced"
queue_type = "simple"
# 高级消息队列配置
broker = "redis://localhost:6379/0"  # 消息队列后端
backend = "redis://localhost:6379/0" # 消息队列结果存储
name = "opengewe_messages"           # 队列名称
concurrency = 4                      # worker并发数量

[gewe]
# 原gewe节配置保持不变
base_url = "http://218.78.116.24:10884/gewe/v2/api"
download_url = ""
callback_url = "http://your_domain_or_ip:5433/api/webhook"
app_id = "wx_12345ABCdeFGhi6789"
token = "1234abcd-1234-1234-1234-1234abcd1234"
is_gewe = true

[plugins]
# 原plugins节配置保持不变
plugins_dir = "plugins"
enabled_plugins = ["ExamplePlugin"]
disabled_plugins = []

[logging]
level = "INFO"            # 日志级别
format = "color"          # 日志格式: "color", "json", "simple"
rotation = "500 MB"       # 日志轮换大小
retention = "10 days"     # 日志保留时间
compression = "zip"       # 日志压缩格式
path = "./logs"           # 日志路径
stdout = true             # 是否输出到控制台
```

## 重构步骤

### 1. 项目初始化

1.1. 创建后端目录结构
```bash
mkdir -p backend/app/{api/{routes},core,db,models,schemas,services,utils,gewe}
mkdir -p backend/tests/{test_api,test_services}
mkdir -p backend/alembic/versions
mkdir -p backend/scripts
```

1.2. 初始化Python包
```bash
touch backend/app/__init__.py
touch backend/app/main.py
touch backend/app/api/__init__.py
touch backend/app/api/routes/__init__.py
touch backend/app/core/__init__.py
touch backend/app/db/__init__.py
touch backend/app/models/__init__.py
touch backend/app/schemas/__init__.py
touch backend/app/services/__init__.py
touch backend/app/utils/__init__.py
touch backend/app/gewe/__init__.py
touch backend/tests/__init__.py
```

1.3. 创建依赖文件
```bash
touch backend/requirements-backend.txt
```

### 2. 核心配置实现 （已完成）

2.1. 实现配置管理
```python
# backend/app/core/config.py
```

2.2. 实现异常处理
```python
# backend/app/core/exceptions.py
```

2.3. 实现安全配置
```python
# backend/app/core/security.py
```

### 3. 数据库实现 （待执行）

3.1. 实现数据库会话
```python
# backend/app/db/session.py
```

3.2. 实现基础模型
```python
# backend/app/db/base.py
```

3.3. 实现数据库初始化
```python
# backend/app/db/init_db.py
```

3.4. 设置Alembic迁移
```python
# backend/alembic/env.py
# backend/alembic.ini
```

### 4. 模型实现

4.1. 实现插件模型
```python
# backend/app/models/plugin.py
```

4.2. 实现机器人模型
```python
# backend/app/models/robot.py
```

4.3. 实现用户模型
```python
# backend/app/models/user.py
```

4.4. 实现配置模型
```python
# backend/app/models/config.py
```

### 5. Schema实现

5.1. 实现插件Schema
```python
# backend/app/schemas/plugin.py
```

5.2. 实现机器人Schema
```python
# backend/app/schemas/robot.py
```

5.3. 实现用户Schema
```python
# backend/app/schemas/user.py
```

5.4. 实现配置Schema
```python
# backend/app/schemas/config.py
```

### 6. 工具函数实现

6.1. 实现Redis管理器
```python
# backend/app/utils/redis_manager.py
```

6.2. 实现日志配置
```python
# backend/app/utils/logger_config.py
```

### 7. GeweClient集成实现

7.1. 实现客户端工厂
```python
# backend/app/gewe/client_factory.py
```

7.2. 实现客户端管理器
```python
# backend/app/gewe/client_manager.py
```

### 8. 服务实现

8.1. 实现插件服务
```python
# backend/app/services/plugin_service.py
```

8.2. 实现机器人服务
```python
# backend/app/services/robot_service.py
```

8.3. 实现管理服务
```python
# backend/app/services/admin_service.py
```

8.4. 实现文件服务
```python
# backend/app/services/file_service.py
```

### 9. API路由实现

9.1. 实现依赖注入
```python
# backend/app/api/deps.py
```

9.2. 实现webhook路由
```python
# backend/app/api/routes/webhook.py
```

9.3. 实现插件管理路由
```python
# backend/app/api/routes/plugin.py
```

9.4. 实现文件管理路由
```python
# backend/app/api/routes/file.py
```

9.5. 实现机器人管理路由
```python
# backend/app/api/routes/robot.py
```

9.6. 实现系统管理路由
```python
# backend/app/api/routes/system.py
```

9.7. 实现管理员路由
```python
# backend/app/api/routes/admin.py
```

### 10. 应用入口实现

10.1. 实现主应用入口
```python
# backend/app/main.py
```

### 11. 测试实现

11.1. 设置测试配置
```python
# backend/tests/conftest.py
```

11.2. 实现API测试
```python
# backend/tests/test_api/*.py
```

11.3. 实现服务测试
```python
# backend/tests/test_services/*.py
```

### 12. 部署脚本

12.1. 实现用户创建脚本
```python
# backend/scripts/create_user.py
```

12.2. 实现数据库初始化脚本
```python
# backend/scripts/init_db.py
```

## 集成策略

### GeweClient集成

1. **客户端工厂模式**：
   - 创建 `ClientFactory` 类，负责根据配置创建 GeweClient 实例
   - 实现客户端池，缓存已创建的客户端实例

2. **多客户端管理**：
   - 创建 `ClientManager` 类，负责管理多个 GeweClient 实例
   - 实现客户端健康检查和自动重连功能

3. **插件系统集成**：
   - 保持原有插件系统的加载和管理逻辑
   - 通过数据库记录插件状态和配置

### 回调处理

1. **异步处理链**：
   - 实现非阻塞的回调处理流程
   - 利用 FastAPI 的后台任务特性

2. **消息分发**：
   - 将回调消息分发给相应的 GeweClient 和插件
   - 实现消息处理的优先级和超时控制

## 自定义日志实现方案

1. **集成 OpenGewe 日志系统**：
   - 利用 `opengewe.logger` 模块的扩展性
   - 创建自定义 logger 配置

2. **结构化日志**：
   - 实现 JSON 格式的结构化日志
   - 添加请求 ID、客户端 ID 等上下文信息

3. **日志分级和分类**：
   - 按功能模块分类日志
   - 实现不同日志级别的控制

4. **日志轮转和压缩**：
   - 实现按大小或时间的日志轮转
   - 实现自动压缩和清理历史日志

## Redis集成初步方案

1. **连接管理**：
   - 创建 `RedisManager` 类，管理 Redis 连接池
   - 实现异步 Redis 操作接口

2. **状态存储**：
   - 设计机器人状态的 Redis 存储结构
   - 实现高效的状态查询和更新接口

3. **分布式锁**：
   - 实现基于 Redis 的分布式锁机制
   - 确保关键操作的并发安全

4. **事件订阅**：
   - 利用 Redis 的发布/订阅功能
   - 实现系统内各组件间的事件通知

## 任务分解与优先级

### 1. 基础设施 (高优先级)
1.1. 目录结构创建
1.2. 核心配置实现
1.3. 数据库连接和模型定义
1.4. 日志系统集成和扩展

### 2. 核心功能 (高优先级)
2.1. 机器人客户端管理
2.2. 回调处理接口
2.3. 文件下载接口
2.4. 插件加载和管理

### 3. 管理功能 (中优先级)
3.1. 机器人状态管理
3.2. 系统配置管理
3.3. 用户认证和授权

### 4. 扩展功能 (低优先级)
4.1. Redis状态存储
4.2. 高级日志分析
4.3. 健康监控和告警
4.4. API文档和客户端SDK

## 风险与挑战

1. **兼容性风险**：
   - 现有插件可能依赖旧的回调处理逻辑
   - 需确保新架构与现有插件的兼容性

2. **性能风险**：
   - 数据库操作可能影响回调处理性能
   - 需实现异步处理和队列机制

3. **扩展性挑战**：
   - 预留足够的扩展点以适应未来需求
   - 避免早期过度设计导致的复杂性

4. **集成挑战**：
   - 与现有 OpenGewe 包的松耦合集成
   - 确保 API 变更不影响现有功能

## 实施检查清单

1. 创建项目目录结构
2. 实现核心配置和异常处理
3. 设置数据库连接和模型
4. 实现基础服务层
5. 实现API路由
6. 集成GeweClient
7. 实现插件管理系统
8. 集成日志系统
9. 实现基本Redis支持
10. 编写测试和文档
11. 部署和性能测试
12. 与前端集成 
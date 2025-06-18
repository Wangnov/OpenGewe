# OpenGewe 后端测试指南

## 快速开始

### 1. 配置测试环境

首先，复制测试配置示例文件：

```bash
cd backend
cp test_config.example.toml test_config.toml
```

然后编辑 `test_config.toml`，修改为您的测试环境配置：

```toml
[test_database]
type = "mysql"
host = "localhost"
port = 3306
username = "your_db_user"
password = "your_db_password"
database = "opengewe_test"

[test_redis]
host = "localhost"
port = 6379
db = 1  # 使用不同的数据库避免与生产环境冲突
```

### 2. 安装测试依赖

```bash
pip install pytest pytest-asyncio httpx
```

### 3. 运行测试

运行所有测试：
```bash
pytest
```

运行特定模块的测试：
```bash
pytest tests/test_auth/
```

运行单个测试文件：
```bash
pytest tests/test_auth/test_auth_api.py
```

显示详细输出：
```bash
pytest -v
```

显示测试覆盖率：
```bash
pytest --cov=app tests/
```

## 配置文件说明

测试配置文件支持以下查找顺序：
1. `tests/test_config.toml` - tests 目录下
2. `backend/test_config.toml` - backend 目录下
3. 环境变量 `TEST_CONFIG_PATH` 指定的路径

您也可以通过环境变量指定配置文件路径：
```bash
export TEST_CONFIG_PATH=/path/to/your/test_config.toml
pytest
```

## 测试结构

```
tests/
├── __init__.py
├── conftest.py          # pytest 配置和共享 fixtures
├── test_auth/           # 认证相关测试
│   ├── __init__.py
│   ├── test_auth_api.py # API 端点测试
│   ├── test_security.py # 安全功能测试
│   └── test_rate_limiter.py # 速率限制测试
└── utils/               # 测试工具
    └── __init__.py
```

## 编写测试

### 使用 fixtures

conftest.py 提供了多个有用的 fixtures：

- `test_session`: 异步数据库会话
- `async_client`: 异步 HTTP 客户端
- `test_user`: 普通测试用户
- `test_superadmin`: 超级管理员用户
- `auth_headers`: 普通用户认证头
- `admin_auth_headers`: 管理员认证头

示例：
```python
async def test_protected_endpoint(async_client, auth_headers):
    response = await async_client.get(
        "/api/v1/auth/me",
        headers=auth_headers
    )
    assert response.status_code == 200
```

### 注意事项

1. **数据库隔离**: 每个测试使用独立的数据库事务，测试结束后自动回滚
2. **速率限制**: 每个测试前后会自动清理速率限制器状态
3. **异步测试**: 使用 `async def` 和 `pytest.mark.asyncio` 标记异步测试

## 常见问题

### 1. 数据库连接错误
确保 MySQL 服务正在运行，并且配置文件中的连接信息正确。

### 2. Redis 连接错误
确保 Redis 服务正在运行，并且配置的数据库号没有被其他服务使用。

### 3. 测试数据库权限
确保数据库用户有创建和删除数据库的权限：
```sql
GRANT ALL PRIVILEGES ON opengewe_test.* TO 'your_user'@'localhost';
GRANT CREATE, DROP ON *.* TO 'your_user'@'localhost';
``` 
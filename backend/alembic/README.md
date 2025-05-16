# 数据库迁移说明

本项目使用Alembic进行数据库迁移管理。Alembic可以跟踪、应用和版本化数据库变更。

## 目录结构

```
alembic/
  ├─ versions/        # 存放迁移脚本
  ├─ env.py          # 环境配置
  ├─ README.md       # 本说明文件
  └─ script.py.mako  # 迁移脚本模板
```

## 使用方法

我们提供了简便的脚本来运行常见的迁移操作，位于 `backend/scripts/run_migrations.py`。

### 创建迁移

当你修改了数据模型后，需要创建迁移脚本来同步数据库结构：

```bash
python backend/scripts/run_migrations.py create "迁移说明"
```

这会在 `alembic/versions/` 目录下创建一个新的迁移脚本文件。

### 应用迁移

将数据库升级到最新版本：

```bash
python backend/scripts/run_migrations.py upgrade
```

升级到特定版本：

```bash
python backend/scripts/run_migrations.py upgrade --revision 版本ID
```

### 回滚迁移

回滚最后一个迁移：

```bash
python backend/scripts/run_migrations.py downgrade
```

回滚到特定版本：

```bash
python backend/scripts/run_migrations.py downgrade --revision 版本ID
```

### 查看迁移信息

显示迁移历史：

```bash
python backend/scripts/run_migrations.py history
```

显示当前版本：

```bash
python backend/scripts/run_migrations.py current
```

## 多Schema支持

本项目支持多schema环境，每个设备使用独立的schema。迁移操作将自动应用到所有配置的设备schema中。

## 注意事项

1. 每次修改模型后，都应该创建新的迁移脚本
2. 在应用迁移前，请确保已备份数据库
3. 复杂的数据迁移可能需要手动编辑自动生成的迁移脚本 
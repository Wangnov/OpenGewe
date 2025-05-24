# OpenGewe 多微信机器人管理后台开发计划

## 📋 项目概述

### 项目目标
开发一个现代化的、移动端兼容的多微信机器人管理后台，深度集成 OpenGewe 框架，提供全面的微信机器人管理功能。

### 项目特点
- **多机器人管理**：支持同时管理多个微信机器人实例
- **现代化界面**：响应式设计，同时支持桌面端和移动端
- **深度集成**：充分利用 OpenGewe 的异步特性、消息处理和插件系统
- **实时通信**：WebSocket 支持实时消息展示

## 🏗️ 系统架构设计

### 整体架构图
```
┌──────────────────────────────────────────────────────────────┐
│                        前端 (React + TS)                     │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │   管理员界面     │ │   机器人管理     │ │   聊天界面      │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                              │ HTTP/WebSocket
┌──────────────────────────────────────────────────────────────┐
│                     后端 (FastAPI)                           │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │  Webhook 接口    │ │  RESTful API   │ │  WebSocket 服务  │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │ GeweClient 池   │ │  插件管理器      │ │  消息处理器      │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                              │
┌──────────────────────────────────────────────────────────────┐
│                    数据库层 (MySQL)                           │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │   管理员数据     │ │ bot_app_id_abc  │ │  bot_app_id_xyz │ │
│  │     Schema      │ │     Schema      │ │     Schema      │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                              │
┌──────────────────────────────────────────────────────────────┐
│                    外部服务集成                               │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│  │    GeWeAPI      │ │     Redis       │ │   RabbitMQ      │ │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

## 🛠️ 技术栈详细说明

### 前端技术栈
```typescript
// 核心框架
React 18+ + TypeScript 5+

// UI 组件库
Ant Design 5.25 (桌面端主要)
Ant Design Mobile 5.x (移动端补充)

// 状态管理
Zustand 4.x (轻量级状态管理)

// 数据请求
React Query/TanStack Query 5.x (数据获取和缓存)

// 路由
React Router 6.x

// 构建工具
Vite 5.x + SWC

// 代码质量
ESLint + Prettier + Husky
TypeScript strict mode

// 样式方案
CSS Modules + Tailwind CSS

// 实时通信
Socket.IO Client

// 图表库
Apache ECharts (消息统计图表)
```

### 后端技术栈
```python
# 核心框架
FastAPI 0.115+ + Python 3.13+

# 微信机器人框架
OpenGewe 0.1.1+ (作为第三方库)

# 数据库
SQLAlchemy 2.x (异步模式)
Pydantic 2.x (数据校验)
MySQL 8+

# 任务队列
Celery + Redis + RabbitMQ

# 认证授权
python-jose (JWT)
passlib (密码哈希)

# WebSocket
FastAPI WebSocket + Socket.IO

# 配置管理
python-decouple (环境变量)
tomli (TOML 配置文件)

# 日志
Loguru (集成 OpenGewe 日志系统)

# 其他工具
aiofiles (异步文件操作)
aioredis (异步 Redis 客户端)
aiomysql (异步 MySQL 客户端)
```

## 🗄️ 数据库设计详解

### 全局管理员数据库 (`admin_data`)

#### 管理员表 (`admins`)
```sql
CREATE TABLE admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    is_superadmin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP NULL,
    
    INDEX idx_username (username),
);
```

#### 管理员登录日志表 (`admin_login_logs`)
```sql
CREATE TABLE admin_login_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    admin_id INT NOT NULL,
    login_ip VARCHAR(45),
    user_agent TEXT,
    login_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('success', 'failed') NOT NULL,
    failure_reason VARCHAR(255),
    
    FOREIGN KEY (admin_id) REFERENCES admins(id) ON DELETE CASCADE,
    INDEX idx_admin_id (admin_id),
    INDEX idx_login_at (login_at)
);
```

#### 全局插件配置表 (`global_plugins`)
```sql
CREATE TABLE global_plugins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    plugin_name VARCHAR(100) UNIQUE NOT NULL,
    is_globally_enabled BOOLEAN DEFAULT TRUE,
    global_config_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_plugin_name (plugin_name)
);
```

### 机器人实例数据库 (每个 Schema: `bot_{app_id}`)

#### 机器人信息表 (`bot_info`)
```sql
CREATE TABLE bot_info (
    bot_wxid VARCHAR(50) PRIMARY KEY,
    gewe_app_id VARCHAR(100) UNIQUE NOT NULL,
    gewe_token VARCHAR(255) NOT NULL,
    nickname VARCHAR(100),
    avatar_url TEXT,
    qr_code_url TEXT,
    is_online BOOLEAN DEFAULT FALSE,
    last_seen_at TIMESTAMP NULL,
    callback_url_override VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_gewe_app_id (gewe_app_id),
    INDEX idx_is_online (is_online)
);
```

#### 原始回调消息表 (`raw_callback_log`)
```sql
CREATE TABLE raw_callback_log (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    bot_wxid VARCHAR(50),
    gewe_appid VARCHAR(100) NOT NULL,
    type_name VARCHAR(50) NOT NULL,
    msg_id VARCHAR(100),
    new_msg_id VARCHAR(100),
    from_wxid VARCHAR(100),
    to_wxid VARCHAR(100),
    raw_json_data JSON NOT NULL,
    processed BOOLEAN DEFAULT FALSE,
    
    INDEX idx_received_at (received_at),
    INDEX idx_bot_wxid (bot_wxid),
    INDEX idx_gewe_appid_type (gewe_appid, type_name),
    INDEX idx_msg_id (msg_id),
    INDEX idx_new_msg_id (new_msg_id),
    INDEX idx_chat_pair (from_wxid, to_wxid),
    INDEX idx_processed (processed)
);
```

#### 联系人表 (`contacts`)
```sql
CREATE TABLE contacts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    bot_wxid VARCHAR(50) NOT NULL,
    contact_wxid VARCHAR(100) NOT NULL,
    contact_type ENUM('friend', 'group', 'public_account', 'enterprise') NOT NULL,
    nickname VARCHAR(200),
    remark VARCHAR(200),
    alias VARCHAR(100),
    big_head_img_url TEXT,
    small_head_img_url TEXT,
    signature TEXT,
    sex TINYINT,
    country VARCHAR(50),
    province VARCHAR(50),
    city VARCHAR(50),
    is_deleted BOOLEAN DEFAULT FALSE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_bot_contact (bot_wxid, contact_wxid),
    INDEX idx_contact_type (contact_type),
    INDEX idx_nickname (nickname),
    INDEX idx_is_deleted (is_deleted)
);
```

#### 群成员表 (`group_members`)
```sql
CREATE TABLE group_members (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    bot_wxid VARCHAR(50) NOT NULL,
    group_wxid VARCHAR(100) NOT NULL,
    member_wxid VARCHAR(100) NOT NULL,
    nickname VARCHAR(200),
    display_name VARCHAR(200),
    is_admin BOOLEAN DEFAULT FALSE,
    is_owner BOOLEAN DEFAULT FALSE,
    join_time TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_group_member (bot_wxid, group_wxid, member_wxid),
    INDEX idx_group_wxid (group_wxid),
    INDEX idx_member_wxid (member_wxid),
    INDEX idx_is_admin (is_admin),
    INDEX idx_is_active (is_active)
);
```

#### 机器人插件配置表 (`bot_plugins`)
```sql
CREATE TABLE bot_plugins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    bot_wxid VARCHAR(50) NOT NULL,
    plugin_name VARCHAR(100) NOT NULL,
    is_enabled BOOLEAN DEFAULT TRUE,
    config_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY uk_bot_plugin (bot_wxid, plugin_name),
    INDEX idx_plugin_name (plugin_name),
    INDEX idx_is_enabled (is_enabled)
);
```

#### 朋友圈记录表 (`sns_posts`)
```sql
CREATE TABLE sns_posts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    bot_wxid VARCHAR(50) NOT NULL,
    sns_id BIGINT NOT NULL,
    author_wxid VARCHAR(100) NOT NULL,
    content TEXT,
    media_urls JSON,
    post_type ENUM('text', 'image', 'video', 'link', 'finder') NOT NULL,
    like_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,
    create_time TIMESTAMP NOT NULL,
    privacy_settings JSON,
    raw_data JSON,
    
    UNIQUE KEY uk_bot_sns (bot_wxid, sns_id),
    INDEX idx_author_wxid (author_wxid),
    INDEX idx_create_time (create_time),
    INDEX idx_post_type (post_type)
);
```

## 📱 功能模块详细规划

### 1. 认证与授权模块

#### 1.1 管理员登录
**前端实现：**
```typescript
// 登录表单组件
interface LoginForm {
  username: string;
  password: string;
  remember?: boolean;
}

// 认证状态管理
interface AuthState {
  isAuthenticated: boolean;
  user: Admin | null;
  token: string | null;
}
```

**后端接口：**
```python
# 登录接口
POST /api/auth/login
{
  "username": "admin",
  "password": "password"
}

# 响应
{
  "access_token": "jwt_token",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "is_superadmin": true
  }
}
```

#### 1.2 权限控制
- **超级管理员**：所有权限
- **普通管理员**：只能管理指定的机器人实例
- **JWT 中间件**：验证所有 API 请求
- **路由守卫**：前端路由级别的权限控制

### 2. 机器人实例管理模块

#### 2.1 机器人列表页面
**功能特性：**
- 卡片式展示所有机器人实例
- 实时显示在线状态（WebSocket 更新）
- 搜索和筛选功能
- 批量操作（启用/禁用）

**前端组件结构：**
```typescript
interface BotInstance {
  botWxid: string;
  geweAppId: string;
  nickname: string;
  avatarUrl: string;
  isOnline: boolean;
  lastSeenAt: string;
  messageCount24h: number;
}

// 机器人卡片组件
const BotCard: React.FC<{ bot: BotInstance }> = ({ bot }) => {
  // 实现卡片显示逻辑
};
```

#### 2.2 添加机器人流程
**步骤设计：**
1. **输入基本信息**：`gewe_app_id` 和 `gewe_token`
2. **验证连接**：测试与 GeWeAPI 的连接
3. **获取机器人信息**：自动获取昵称、头像等
4. **初始化数据库**：创建专属 Schema
5. **同步联系人**：后台异步同步联系人和群聊数据

**后端实现逻辑：**
```python
@router.post("/bots")
async def create_bot(bot_data: BotCreateRequest):
    # 1. 验证 GeweClient 连接
    client = GeweClient(
        base_url="http://www.geweapi.com/gewe/v2/api",
        app_id=bot_data.gewe_app_id,
        token=bot_data.gewe_token,
        is_gewe=True
    )
    
    # 2. 检查在线状态
    online_status = await client.account.check_online()
    if not online_status.get("data"):
        raise HTTPException(400, "机器人离线或配置错误")
    
    # 3. 获取机器人信息
    profile = await client.personal.get_profile()
    
    # 4. 创建数据库 Schema
    await create_bot_schema(profile["data"]["wxid"])
    
    # 5. 保存机器人信息
    bot_info = await save_bot_info(profile["data"])
    
    # 6. 启动后台同步任务
    sync_contacts_task.delay(bot_info.bot_wxid)
    
    return bot_info
```

### 3. 聊天管理模块

#### 3.1 聊天界面设计
**布局结构：**
```
┌─────────────────────────────────────────────────────────────┐
│                     聊天管理界面                            │
├──────────────┬────────────────────────────────────────────┤
│              │                聊天窗口                     │
│   联系人列表  │  ┌──────────────────────────────────────┐   │
│              │  │          消息历史记录                │   │
│  🔍 搜索框    │  │                                      │   │
│              │  └──────────────────────────────────────┘   │
│  📱 张三      │  ┌──────────────────────────────────────┐   │
│  🏢 工作群    │  │          消息输入框                  │   │
│  👥 朋友群    │  │  📎 📷 🎤 😊              发送       │   │
│  ...         │  └──────────────────────────────────────┘   │
└──────────────┴────────────────────────────────────────────┘
```

#### 3.2 消息类型支持
**支持的消息类型：**
- ✅ 文本消息（支持 @ 功能）
- ✅ 图片消息（支持拖拽上传）
- ✅ 语音消息（录音功能）
- ✅ 视频消息
- ✅ 文件消息
- ✅ 表情消息
- ✅ 链接消息
- ✅ 名片消息
- ⭐ 引用回复
- ⭐ 消息撤回

**前端消息组件：**
```typescript
interface Message {
  id: string;
  type: MessageType;
  content: string;
  fromWxid: string;
  toWxid: string;
  timestamp: number;
  isFromSelf: boolean;
  status: 'sending' | 'sent' | 'failed';
  media?: {
    url: string;
    thumbnail?: string;
    size?: number;
    duration?: number;
  };
}

const MessageBubble: React.FC<{ message: Message }> = ({ message }) => {
  // 根据消息类型渲染不同的气泡样式
};
```

#### 3.3 实时消息处理
**WebSocket 消息流：**
```typescript
// WebSocket 事件类型
interface WebSocketEvents {
  'new_message': Message;
  'message_status_update': { messageId: string; status: string };
  'bot_status_change': { botWxid: string; isOnline: boolean };
  'typing_indicator': { chatId: string; userWxid: string; isTyping: boolean };
}

// WebSocket 连接管理
class WebSocketManager {
  private socket: Socket;
  
  connect(token: string) {
    this.socket = io('/chat', {
      auth: { token },
      transports: ['websocket']
    });
  }
  
  subscribeToBot(botWxid: string) {
    this.socket.emit('subscribe_bot', { botWxid });
  }
}
```

### 4. 朋友圈管理模块

#### 4.1 朋友圈发布功能
**发布类型：**
- 纯文本朋友圈
- 图片朋友圈（支持多图）
- 视频朋友圈
- 链接朋友圈

**前端发布组件：**
```typescript
interface SnsPostData {
  content: string;
  type: 'text' | 'image' | 'video' | 'link';
  mediaFiles?: File[];
  privacy: {
    allowWxids?: string[];
    disableWxids?: string[];
    allowTagIds?: string[];
    disableTagIds?: string[];
    isPrivate: boolean;
  };
  location?: string;
  atWxids?: string[];
}

const SnsPublisher: React.FC = () => {
  // 朋友圈发布组件实现
};
```

#### 4.2 朋友圈浏览功能
- 查看自己发布的朋友圈
- 浏览好友朋友圈
- 点赞和评论功能
- 朋友圈数据同步

### 5. 插件管理模块

#### 5.1 全局插件管理
**功能列表：**
- 插件列表展示（从 `plugins` 目录扫描）
- 全局启用/禁用插件
- 插件配置管理
- 插件上传功能（可选）

**插件信息结构：**
```typescript
interface PluginInfo {
  name: string;
  description: string;
  author: string;
  version: string;
  isGloballyEnabled: boolean;
  configSchema?: JSONSchema;
  globalConfig?: Record<string, any>;
  enabledBots: string[];
  totalBots: number;
}
```

#### 5.2 机器人级别插件配置
- 继承全局配置
- 覆盖特定机器人配置
- 插件配置验证
- 配置变更实时生效

### 6. 统计与监控模块

#### 6.1 数据统计功能
**统计维度：**
- 消息量统计（24小时、7天、30天）
- 活跃联系人统计
- 插件使用统计
- 错误日志统计

**图表展示：**
```typescript
interface StatisticsData {
  messageStats: {
    total: number;
    byType: Record<string, number>;
    trend: Array<{ date: string; count: number }>;
  };
  contactStats: {
    totalFriends: number;
    totalGroups: number;
    activeContacts: number;
  };
  pluginStats: {
    enabledCount: number;
    totalCount: number;
    usage: Array<{ plugin: string; calls: number }>;
  };
}
```

#### 6.2 系统监控
- 机器人在线状态监控
- 消息处理延迟监控
- 错误率监控
- 系统资源使用监控

## 🚀 开发阶段规划

### 第一阶段：基础架构（4-6周）

#### Week 1-2: 项目初始化与后端基础
**任务清单：**
- [ ] 创建项目仓库和目录结构
- [ ] 配置开发环境（Docker Compose）
- [ ] 搭建 FastAPI 基础框架
- [ ] 实现数据库连接和模型定义
- [ ] 完成 JWT 认证系统
- [ ] 实现基础的 CRUD 操作

**技术要点：**
```python
# 项目结构
backend/
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── bots.py
│   │   ├── webhooks.py
│   │   └── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── models/
│   ├── schemas/
│   └── services/
└── requirements.txt
```

#### Week 3-4: 前端基础与路由
**任务清单：**
- [ ] 创建 React + TypeScript 项目
- [ ] 配置 Vite 构建工具
- [ ] 搭建基础路由结构
- [ ] 实现登录页面和认证流程
- [ ] 创建主要页面框架
- [ ] 配置状态管理（Zustand）

**前端结构：**
```typescript
src/
├── components/
│   ├── common/
│   ├── auth/
│   └── layout/
├── pages/
│   ├── Login.tsx
│   ├── Dashboard.tsx
│   ├── BotManagement.tsx
│   └── ChatInterface.tsx
├── hooks/
├── stores/
├── utils/
└── types/
```

### 第二阶段：核心功能开发（6-8周）

#### Week 5-6: 机器人管理功能
**后端任务：**
- [ ] 实现 GeweClient 实例池管理
- [ ] 完成机器人 CRUD 接口
- [ ] 实现动态数据库 Schema 创建
- [ ] 集成 OpenGewe 客户端

**前端任务：**
- [ ] 实现机器人列表页面
- [ ] 创建添加机器人流程
- [ ] 实现机器人状态监控
- [ ] 添加机器人操作功能

#### Week 7-8: Webhook 与消息处理
**核心功能：**
- [ ] 实现 Webhook 接收接口
- [ ] 完成消息存储逻辑
- [ ] 实现消息分发机制
- [ ] 集成 OpenGewe MessageFactory

**技术实现：**
```python
@app.post("/webhook/{bot_schema_id}")
async def webhook_handler(
    bot_schema_id: str,
    payload: Dict[str, Any],
    request: Request
):
    # 1. 验证来源
    await verify_webhook_source(request)
    
    # 2. 存储原始消息
    await store_raw_callback(bot_schema_id, payload)
    
    # 3. 分发给 MessageFactory
    client = get_bot_client(bot_schema_id)
    await client.message_factory.process(payload)
    
    return {"status": "ok"}
```

#### Week 9-10: 聊天界面基础
**功能实现：**
- [ ] 联系人列表组件
- [ ] 聊天窗口布局
- [ ] 消息气泡组件
- [ ] 基础消息发送功能

#### Week 11-12: 实时通信
**WebSocket 实现：**
- [ ] 搭建 WebSocket 服务
- [ ] 实现消息实时推送
- [ ] 添加在线状态同步
- [ ] 实现消息状态更新

### 第三阶段：高级功能（4-6周）

#### Week 13-14: 朋友圈管理
- [ ] 朋友圈发布功能
- [ ] 朋友圈浏览界面
- [ ] 媒体文件上传处理
- [ ] 朋友圈数据同步

#### Week 15-16: 插件管理系统
- [ ] 插件扫描和加载
- [ ] 插件配置界面
- [ ] 全局和实例级配置
- [ ] 插件状态管理

#### Week 17-18: 统计与监控
- [ ] 数据统计收集
- [ ] 图表展示组件
- [ ] 系统监控面板
- [ ] 日志查看功能

### 第四阶段：优化与部署（2-4周）

#### Week 19-20: 性能优化
- [ ] 前端代码分割和懒加载
- [ ] 后端查询优化
- [ ] 缓存策略实现
- [ ] 内存和性能监控

#### Week 21-22: 测试与部署
- [ ] 单元测试和集成测试
- [ ] 部署脚本编写
- [ ] Docker 镜像构建
- [ ] 生产环境配置

## 🔧 关键技术实现要点

### 1. GeweClient 实例池管理

```python
class BotClientManager:
    def __init__(self):
        self._clients: Dict[str, GeweClient] = {}
        self._client_configs: Dict[str, Dict] = {}
    
    async def get_client(self, bot_wxid: str) -> GeweClient:
        """获取或创建 GeweClient 实例"""
        if bot_wxid not in self._clients:
            config = await self._load_bot_config(bot_wxid)
            client = GeweClient(**config)
            self._clients[bot_wxid] = client
            await self._initialize_client(client)
        
        return self._clients[bot_wxid]
    
    async def remove_client(self, bot_wxid: str):
        """安全移除客户端实例"""
        if bot_wxid in self._clients:
            await self._clients[bot_wxid].close()
            del self._clients[bot_wxid]
    
    async def reload_client(self, bot_wxid: str):
        """重新加载客户端配置"""
        await self.remove_client(bot_wxid)
        return await self.get_client(bot_wxid)
```

### 2. 动态数据库 Schema 管理

```python
class DatabaseManager:
    async def create_bot_schema(self, bot_wxid: str):
        """为新机器人创建独立的数据库 Schema"""
        schema_name = f"bot_{bot_wxid.replace('@', '_')}"
        
        # 创建 Schema
        await self.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
        
        # 创建表结构
        await self._create_bot_tables(schema_name)
        
        return schema_name
    
    async def get_bot_engine(self, bot_wxid: str):
        """获取特定机器人的数据库连接"""
        schema_name = f"bot_{bot_wxid.replace('@', '_')}"
        return create_async_engine(
            f"mysql+aiomysql://user:pass@host:port/{schema_name}"
        )
```

### 3. 消息处理管道

```python
class MessageProcessor:
    def __init__(self, bot_manager: BotClientManager):
        self.bot_manager = bot_manager
    
    async def process_webhook(self, bot_schema_id: str, payload: Dict):
        """处理 Webhook 消息"""
        # 1. 数据验证和清洗
        validated_payload = await self._validate_payload(payload)
        
        # 2. 存储原始消息
        message_id = await self._store_raw_message(
            bot_schema_id, validated_payload
        )
        
        # 3. 消息去重检查
        if await self._is_duplicate_message(message_id):
            return
        
        # 4. 分发给 OpenGewe
        client = await self.bot_manager.get_client(bot_schema_id)
        await client.message_factory.process(validated_payload)
        
        # 5. 实时推送给前端
        await self._broadcast_message(bot_schema_id, validated_payload)
```

### 4. WebSocket 消息分发

```python
class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """建立 WebSocket 连接"""
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
    
    async def broadcast_to_bot_subscribers(
        self, bot_wxid: str, message: Dict
    ):
        """向订阅特定机器人的用户广播消息"""
        for user_id, connections in self.active_connections.items():
            if await self._user_has_bot_access(user_id, bot_wxid):
                for connection in connections:
                    await connection.send_json(message)
```

### 5. 安全机制实现

```python
# JWT 认证中间件
async def verify_token(request: Request):
    """验证 JWT Token"""
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(401, "未提供有效的认证令牌")
    
    try:
        payload = jwt.decode(
            token.replace("Bearer ", ""),
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "无效的令牌")
        
        return user_id
    except JWTError:
        raise HTTPException(401, "令牌验证失败")

# Webhook 来源验证
async def verify_webhook_source(request: Request):
    """验证 Webhook 来源"""
    # 1. IP 白名单检查
    client_ip = request.client.host
    if not await is_whitelisted_ip(client_ip):
        raise HTTPException(403, "IP 地址未授权")
    
    # 2. 签名验证（如果 GeWeAPI 提供）
    signature = request.headers.get("X-Gewe-Signature")
    if signature:
        body = await request.body()
        expected_signature = generate_signature(body)
        if not hmac.compare_digest(signature, expected_signature):
            raise HTTPException(403, "签名验证失败")
```

## 📦 部署与运维策略

### 1. Docker 容器化部署

```dockerfile
# 后端 Dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# 前端 Dockerfile
FROM node:20-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
```

### 2. Docker Compose 配置

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+aiomysql://user:pass@mysql:3306/opengewe
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - mysql
      - redis
    volumes:
      - ./logs:/app/logs
      - ./plugins:/app/plugins

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  mysql:
    image: mysql:9.3
    environment:
      - MYSQL_ROOT_PASSWORD=rootpass
      - MYSQL_DATABASE=opengewe
      - MYSQL_USER=user
      - MYSQL_PASSWORD=pass
    volumes:
      - mysql_data:/var/lib/mysql
      - ./mysql/init:/docker-entrypoint-initdb.d

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  rabbitmq:
    image: rabbitmq:3-management
    environment:
      - RABBITMQ_DEFAULT_USER=user
      - RABBITMQ_DEFAULT_PASS=pass
    ports:
      - "15672:15672"
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

volumes:
  mysql_data:
  redis_data:
  rabbitmq_data:
```

### 3. 监控与日志

```python
# 集成 OpenGewe 日志系统
from opengewe.logger import get_logger, init_default_logger

# 初始化日志系统
init_default_logger(
    level="INFO",
    structured=True,
    config_file="main_config.toml"
)

# 获取专用日志记录器
logger = get_logger("WebPanel.Backend")

# 添加自定义日志处理器
logger.add(
    "logs/webpanel_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO"
)
```

### 4. 配置管理

```toml
# main_config.toml
[webpanel]
secret_key = "your-secret-key"
debug = false
cors_origins = ["http://localhost:3000"]

[webpanel.database]
url = "mysql+aiomysql://user:pass@localhost:3306/opengewe"
pool_size = 10
max_overflow = 20

[webpanel.redis]
url = "redis://localhost:6379/0"
max_connections = 10

[webpanel.security]
jwt_expiration_hours = 24
password_min_length = 8
max_login_attempts = 5

[logging]
level = "INFO"
format = "json"
path = "./logs"
stdout = true
```

## 🔍 测试策略

### 1. 后端测试

```python
# 单元测试示例
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_bot():
    response = client.post(
        "/api/bots",
        json={
            "gewe_app_id": "test_app_id",
            "gewe_token": "test_token"
        },
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code == 200
    assert "bot_wxid" in response.json()

# 集成测试
@pytest.mark.asyncio
async def test_webhook_processing():
    # 模拟 GeWeAPI 回调
    webhook_payload = {
        "Appid": "test_app_id",
        "TypeName": "AddMsg",
        "Data": {
            "MsgType": 1,
            "Content": {"string": "测试消息"},
            # ... 其他字段
        }
    }
    
    response = await client.post(
        "/webhook/test_bot_schema",
        json=webhook_payload
    )
    
    assert response.status_code == 200
    # 验证消息是否正确存储
    # 验证是否正确分发给 MessageFactory
```

### 2. 前端测试

```typescript
// 组件测试
import { render, screen, fireEvent } from '@testing-library/react';
import { BotCard } from '@/components/BotCard';

test('displays bot information correctly', () => {
  const bot = {
    botWxid: 'test_wxid',
    nickname: '测试机器人',
    isOnline: true,
    lastSeenAt: '2024-01-01T00:00:00Z'
  };

  render(<BotCard bot={bot} />);
  
  expect(screen.getByText('测试机器人')).toBeInTheDocument();
  expect(screen.getByText('在线')).toBeInTheDocument();
});

// API 测试
import { rest } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  rest.get('/api/bots', (req, res, ctx) => {
    return res(ctx.json({ bots: [] }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## 📈 性能优化策略

### 1. 数据库优化
- **索引策略**：为常用查询字段添加合适的索引
- **分页查询**：大数据量列表使用游标分页
- **连接池**：使用数据库连接池避免频繁连接
- **读写分离**：考虑读写分离提高查询性能

### 2. 缓存策略
```python
# Redis 缓存实现
from aioredis import Redis

class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis
    
    async def get_bot_info(self, bot_wxid: str):
        """获取机器人信息（带缓存）"""
        cache_key = f"bot_info:{bot_wxid}"
        cached = await self.redis.get(cache_key)
        
        if cached:
            return json.loads(cached)
        
        # 从数据库获取
        bot_info = await fetch_bot_info_from_db(bot_wxid)
        
        # 缓存 1 小时
        await self.redis.setex(
            cache_key, 3600, json.dumps(bot_info)
        )
        
        return bot_info
```

### 3. 前端优化
- **代码分割**：按路由进行代码分割
- **虚拟滚动**：长列表使用虚拟滚动
- **图片懒加载**：聊天记录中的图片懒加载
- **防抖节流**：搜索和输入框使用防抖

## 🔒 安全考虑

### 1. 数据安全
- **数据加密**：敏感数据加密存储
- **输入验证**：严格的输入数据验证
- **SQL 注入防护**：使用参数化查询
- **XSS 防护**：前端输出转义

### 2. 接口安全
- **认证授权**：JWT + RBAC 权限控制
- **HTTPS**：强制使用 HTTPS
- **CORS 配置**：严格的跨域配置
- **API 限流**：防止接口滥用

### 3. Webhook 安全
- **IP 白名单**：限制 Webhook 来源 IP
- **签名验证**：验证请求签名
- **重放攻击防护**：使用时间戳和随机数
- **数据校验**：严格校验 Webhook 数据格式

## 📖 文档与维护

### 1. 开发文档
- **API 文档**：使用 FastAPI 自动生成
- **组件文档**：使用 Storybook 管理组件
- **部署文档**：详细的部署和配置说明
- **故障排除**：常见问题和解决方案

### 2. 代码规范
- **Python**：遵循 PEP 8 + Black 格式化
- **TypeScript**：使用 ESLint + Prettier
- **Git 规范**：Conventional Commits
- **代码审查**：Pull Request 必须审查

### 3. 监控维护
- **健康检查**：定期检查服务状态
- **性能监控**：监控关键指标
- **日志分析**：定期分析日志发现问题
- **备份策略**：定期备份数据库

---

## 总结

这份开发计划涵盖了 OpenGewe 多微信机器人管理后台的完整开发流程，从技术选型到具体实现，从数据库设计到部署运维。通过分阶段的开发方式，确保项目能够稳步推进，同时保证代码质量和系统安全性。

项目的核心价值在于深度集成 OpenGewe 框架，提供现代化的 Web 界面来管理多个微信机器人实例，让用户能够方便地进行聊天、朋友圈管理、插件配置等操作。

**项目估计总开发时间：20-22周**
**建议团队规模：2-3名全栈开发工程师**
**技术难点：GeweClient 实例管理、实时消息处理、多租户数据库设计** 
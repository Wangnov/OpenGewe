# OpenGewe

![版本](https://img.shields.io/badge/版本-0.2.1-blue)
![Python](https://img.shields.io/badge/Python-3.9+-brightgreen)
![协议](https://img.shields.io/badge/协议-MIT-green)

> OpenGewe 是一个功能强大的、基于 GeWeAPI 的异步 Python 微信机器人框架，现已包含一个现代化的前后端分离管理面板，为您提供开箱即用的微信自动化和智能管理解决方案。

## 🌟 项目亮点

- 🚀 **全异步核心**: 基于 `asyncio` 构建，为高并发场景提供卓越性能。
- 💻 **现代化Web面板**: 使用 **React 19 + FastAPI** 构建，提供响应式、用户友好的机器人和插件管理界面。
- 🔌 **强大的插件系统**: 易于扩展的插件架构，支持动态加载、热重载和全局/机器人级别的独立配置。
- 🤖 **企业级多租户**: 为每个机器人实例创建独立的数据库 Schema，实现安全的数据隔离。
- 📨 **全面的消息处理**: 内置所有31种微信回调消息类型的解析和处理，从文本到系统通知，无一遗漏。
- 🛠️ **一键启动**: 提供 `start.sh` 脚本，一键并发启动前后端开发环境。
- 큐 **灵活的消息队列**: 支持轻量级的 `simple` 模式和基于 `Celery` 的 `advanced` 高级模式，满足不同场景需求。

## 📸 界面概览

*(这里可以插入Web管理面板的截图，例如机器人列表、插件管理页面等)*

**登录页面:**
![Login Page](https://your-image-host.com/login.png)

**机器人管理:**
![Bots Dashboard](https://your-image-host.com/bots.png)

**插件中心:**
![Plugins Marketplace](https://your-image-host.com/plugins.png)

## 快速开始

我们提供了一键式脚本来简化开发环境的启动。

```bash
# 1. 克隆项目
git clone https://github.com/Wangnov/OpenGewe.git
cd OpenGewe

# 2. (首次运行) 安装依赖
# 该脚本会自动安装前端和后端所需的所有依赖
./start.sh --install

# 3. (日常启动) 启动开发服务器
# 该脚本会并发启动前端Vite服务和后端FastAPI服务
./start.sh
```

启动后，请访问：
- **前端管理面板**: `http://localhost:5173`
- **后端API文档**: `http://localhost:5432/docs`

## 架构

OpenGewe 采用先进的前后端分离架构，确保了高内聚、低耦合的模块化设计。

*(这里可以插入架构图)*
![Architecture Diagram](https://your-image-host.com/architecture.png)

- **前端 (Frontend)**: 基于 **React 19** 和 **Vite** 构建，负责所有用户交互和数据展示。
- **后端 (Backend)**: 基于 **FastAPI** 构建，提供 RESTful API，处理所有业务逻辑、数据库交互和机器人控制。
- **核心库 (src/opengewe)**: 独立、可发布的 Python 包，封装了与 GeWeAPI 的所有通信和消息处理逻辑。
- **插件 (Plugins)**: 独立的插件目录，允许开发者轻松扩展机器人功能。
- **数据库**: 使用 **MySQL**，通过 SQLAlchemy 进行异步操作，并为每个机器人实例创建独立的 Schema。

## 插件生态

插件是 OpenGewe 的核心扩展方式。我们提供了一系列官方插件，您也可以轻松开发自己的插件。

### 官方插件

- **AIAssistant**: 对接大语言模型，提供智能对话能力。
- **KeywordMonitor**: 监控群聊关键词，实时发送舆情警报。
- **ScheduledTaskNotifier**: 支持通过聊天指令动态创建和管理定时任务。
- **FileAnalyzerAssistant**: 智能分析用户发送的文本文件并生成摘要。
- **DailyQuote**: 提供每日一言功能。
- ... 更多插件正在开发中！

### 开发自己的插件

1.  在 `plugins` 目录下创建一个新的文件夹，例如 `MyAwesomePlugin`。
2.  在文件夹中创建 `main.py` 和 `config.toml`。
3.  在 `main.py` 中，创建一个继承自 `PluginBase` 的类。
4.  使用 `@on_text_message`, `@schedule` 等装饰器来定义您的事件处理函数和定时任务。

详细的插件开发指南请参考 [插件开发文档](link-to-plugin-dev-doc.md)。

## 发展蓝图

本项目正处于高速迭代中，我们有一个清晰的未来发展计划。更多细节请参考我们的 [**未来开发计划文档**](./OpenGewe-WebPanel-Development-Plan.md)。

## 贡献

我们欢迎任何形式的贡献！无论是提交 Issue、发起 Pull Request，还是改进文档，都对我们至关重要。

## 许可证

本项目采用 [MIT 许可证](./LICENSE)。

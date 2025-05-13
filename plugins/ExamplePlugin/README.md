# ExamplePlugin 示例插件

这是一个用于演示OpenGewe插件系统的示例插件。

## 功能特点

- 处理多种类型的消息（文本、图片、视频等）
- 演示不同优先级的使用方法
- 包含多种定时任务示例（间隔执行、定时执行、指定日期执行）
- 演示如何读取配置文件

## 配置说明

配置文件位于 `config.toml`，包含以下选项：

```toml
[basic]
enable = true  # 是否启用插件

[features]
message_response = true  # 是否启用消息响应功能
scheduled_tasks = true   # 是否启用定时任务

[advanced]
debug_mode = false      # 是否启用调试模式
log_level = "info"      # 日志级别
```

## 使用方法

1. 确保配置文件中 `enable = true`
2. 重新加载插件或启动程序
3. 观察日志输出，验证插件的工作状态

## 开发说明

此插件展示了以下开发技巧：

- 如何使用消息处理装饰器
- 如何设置处理优先级
- 如何创建不同类型的定时任务
- 如何读取和使用配置文件
- 如何进行异步初始化

## 作者

Wangnov

## 版本历史

- v1.0.0: 初始版本 
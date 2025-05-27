#!/usr/bin/env python3
"""
插件系统验证脚本
用于验证OpenGewe WebPanel的插件系统是否正常工作
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "webpanel"))

from webpanel.app.services.bot_manager import bot_manager
from webpanel.app.core.session_manager import admin_session
from webpanel.app.models.bot import BotInfo
from sqlalchemy import select


async def verify_plugin_system():
    """验证插件系统是否正常工作"""
    print("🔍 OpenGewe WebPanel 插件系统验证")
    print("=" * 50)

    try:
        # 1. 获取机器人信息
        async with admin_session() as session:
            stmt = select(BotInfo)
            result = await session.execute(stmt)
            bots = result.scalars().all()

            if not bots:
                print("❌ 没有找到机器人配置")
                return False

            test_bot = bots[0]
            print(f"✅ 找到测试机器人: {test_bot.nickname} ({test_bot.gewe_app_id})")

            # 2. 创建客户端并验证插件加载
            client = await bot_manager.get_client(test_bot.gewe_app_id, session)

            if not client:
                print("❌ 无法创建机器人客户端")
                return False

            print("✅ 机器人客户端创建成功")

            # 3. 验证插件管理器
            if not hasattr(client, "plugin_manager"):
                print("❌ 客户端缺少插件管理器")
                return False

            plugin_manager = client.plugin_manager
            print(f"✅ 插件管理器存在: {type(plugin_manager).__name__}")

            # 4. 验证插件注册
            if not hasattr(plugin_manager, "plugins"):
                print("❌ 插件管理器缺少plugins属性")
                return False

            registered_plugins = list(plugin_manager.plugins.keys())
            print(f"✅ 已注册插件: {registered_plugins}")

            if "ExamplePlugin" not in registered_plugins:
                print("❌ ExamplePlugin未注册")
                return False

            # 5. 验证事件管理器
            if not hasattr(plugin_manager, "event_manager"):
                print("❌ 插件管理器缺少事件管理器")
                return False

            event_manager = plugin_manager.event_manager
            print(f"✅ 事件管理器存在: {type(event_manager).__name__}")

            # 6. 验证事件处理器
            if not hasattr(event_manager, "handlers"):
                print("❌ 事件管理器缺少handlers属性")
                return False

            handlers = event_manager.handlers
            total_handlers = sum(
                len(handler_list) for handler_list in handlers.values()
            )
            print(f"✅ 事件处理器总数: {total_handlers}")

            if total_handlers == 0:
                print("❌ 没有注册任何事件处理器")
                return False

            # 7. 验证具体的处理器
            from opengewe.callback.types import MessageType

            if MessageType.TEXT in handlers:
                text_handlers = handlers[MessageType.TEXT]
                print(f"✅ 文本消息处理器数量: {len(text_handlers)}")

                # 检查ExamplePlugin的handle_text方法
                example_plugin = plugin_manager.plugins["ExamplePlugin"]
                if hasattr(example_plugin, "handle_text"):
                    handle_text_method = getattr(example_plugin, "handle_text")
                    if handle_text_method in text_handlers:
                        print("✅ ExamplePlugin.handle_text已正确注册")
                    else:
                        print("⚠️  ExamplePlugin.handle_text未在处理器列表中")
                else:
                    print("❌ ExamplePlugin缺少handle_text方法")
            else:
                print("❌ 没有文本消息处理器")
                return False

            # 8. 验证消息工厂
            if not hasattr(client, "message_factory"):
                print("❌ 客户端缺少消息工厂")
                return False

            print(f"✅ 消息工厂存在: {type(client.message_factory).__name__}")

            # 9. 验证定时任务
            if hasattr(example_plugin, "_scheduled_jobs"):
                scheduled_jobs = example_plugin._scheduled_jobs
                print(f"✅ 定时任务数量: {len(scheduled_jobs)}")
                for job_id in scheduled_jobs:
                    print(f"  - {job_id}")
            else:
                print("⚠️  插件没有定时任务属性")

            print("\n" + "=" * 50)
            print("🎉 插件系统验证完成！")
            print("✅ 所有核心功能正常工作")
            print("✅ ExamplePlugin已成功加载并注册")
            print("✅ 事件处理器已正确配置")
            print("✅ 系统准备接收和处理消息")

            return True

    except Exception as e:
        print(f"❌ 验证过程中发生错误: {e}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """主函数"""
    success = await verify_plugin_system()

    if success:
        print("\n🚀 插件系统验证成功！可以启动WebPanel后端了。")
        sys.exit(0)
    else:
        print("\n💥 插件系统验证失败！请检查配置。")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

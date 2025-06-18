import asyncio
import sys
import os
import time

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "webpanel"))

from webpanel.app.services.bot_manager import bot_manager
from webpanel.app.core.session_manager import admin_session
from webpanel.app.models.bot import BotInfo
from sqlalchemy import select


async def test_plugin_functionality():
    """测试插件功能是否正常工作"""
    print("=== 测试插件功能 ===")

    try:
        # 获取机器人信息并创建客户端
        async with admin_session() as session:
            stmt = select(BotInfo)
            result = await session.execute(stmt)
            bots = result.scalars().all()

            if not bots:
                print("没有找到机器人")
                return

            test_bot = bots[0]
            print(f"测试机器人: {test_bot.gewe_app_id}")

            # 创建客户端
            client = await bot_manager.get_client(test_bot.gewe_app_id, session)

            if not client:
                print("❌ 客户端创建失败")
                return

            print("✅ 客户端创建成功")

            # 检查插件管理器
            if hasattr(client, "plugin_manager"):
                plugin_manager = client.plugin_manager
                print(f"✅ 插件管理器存在: {type(plugin_manager)}")

                # 检查已注册的插件
                if hasattr(plugin_manager, "plugins"):
                    registered_plugins = list(plugin_manager.plugins.keys())
                    print(f"已注册的插件: {registered_plugins}")

                    if "ExamplePlugin" in registered_plugins:
                        plugin_instance = plugin_manager.plugins["ExamplePlugin"]
                        print(f"✅ ExamplePlugin实例: {type(plugin_instance)}")

                        # 检查插件属性
                        print(
                            f"插件启用状态: {getattr(plugin_instance, 'enable', 'unknown')}"
                        )
                        print(f"插件属性: {list(plugin_instance.__dict__.keys())}")

                        # 检查定时任务
                        if hasattr(plugin_instance, "_scheduled_jobs"):
                            scheduled_jobs = plugin_instance._scheduled_jobs
                            print(f"定时任务: {scheduled_jobs}")

                        # 尝试手动调用插件方法
                        try:
                            print("\n测试手动调用插件方法...")

                            # 创建一个模拟消息对象
                            class MockMessage:
                                def __init__(self):
                                    self.content = "测试消息"
                                    self.from_wxid = "test_user"
                                    self.to_wxid = test_bot.gewe_app_id

                            mock_message = MockMessage()

                            # 尝试调用文本消息处理器
                            if hasattr(plugin_instance, "handle_text"):
                                print("调用handle_text方法...")
                                await plugin_instance.handle_text(client, mock_message)
                                print("✅ handle_text方法调用成功")
                            else:
                                print("❌ 插件没有handle_text方法")

                        except Exception as e:
                            print(f"❌ 手动调用插件方法失败: {e}")
                            import traceback

                            traceback.print_exc()

                    else:
                        print("❌ ExamplePlugin未注册")
                else:
                    print("❌ 插件管理器没有plugins属性")

                # 检查调度器
                if hasattr(plugin_manager, "scheduler"):
                    scheduler = plugin_manager.scheduler
                    print(f"✅ 调度器存在: {type(scheduler)}")

                    # 检查调度器中的任务
                    if hasattr(scheduler, "get_jobs"):
                        jobs = scheduler.get_jobs()
                        print(f"调度器中的任务数量: {len(jobs)}")
                        for job in jobs:
                            print(f"  - 任务: {job.id}, 下次执行: {job.next_run_time}")
                    else:
                        print("调度器没有get_jobs方法")
                else:
                    print("❌ 插件管理器没有scheduler属性")

                # 检查事件管理器
                if hasattr(plugin_manager, "event_manager"):
                    event_manager = plugin_manager.event_manager
                    print(f"✅ 事件管理器存在: {type(event_manager)}")

                    if hasattr(event_manager, "handlers"):
                        handlers = event_manager.handlers
                        print(f"事件处理器: {dict(handlers)}")

                        # 检查是否有文本消息处理器
                        from opengewe.callback.models import MessageType

                        if MessageType.TEXT in handlers:
                            text_handlers = handlers[MessageType.TEXT]
                            print(f"文本消息处理器数量: {len(text_handlers)}")
                            for handler in text_handlers:
                                print(f"  - 处理器: {handler}")
                        else:
                            print("❌ 没有文本消息处理器")
                    else:
                        print("❌ 事件管理器没有handlers属性")
                else:
                    print("❌ 插件管理器没有event_manager属性")

                # 尝试启动插件管理器
                try:
                    if hasattr(plugin_manager, "start_all_plugins"):
                        print("\n启动插件管理器...")
                        await plugin_manager.start_all_plugins()
                        print("✅ 插件管理器启动成功")

                        # 再次检查事件管理器
                        if hasattr(plugin_manager, "event_manager"):
                            event_manager = plugin_manager.event_manager
                            if hasattr(event_manager, "handlers"):
                                handlers = event_manager.handlers
                                print(f"启动后的事件处理器: {dict(handlers)}")

                    else:
                        print("插件管理器没有start_all_plugins方法")
                except Exception as e:
                    print(f"启动插件管理器失败: {e}")
                    import traceback

                    traceback.print_exc()

            else:
                print("❌ 客户端没有plugin_manager属性")

    except Exception as e:
        print(f"测试失败: {e}")
        import traceback

        traceback.print_exc()


async def test_message_processing():
    """测试消息处理功能"""
    print("\n=== 测试消息处理功能 ===")

    try:
        async with admin_session() as session:
            stmt = select(BotInfo)
            result = await session.execute(stmt)
            bots = result.scalars().all()

            if not bots:
                print("没有找到机器人")
                return

            test_bot = bots[0]

            # 模拟webhook消息
            mock_payload = {
                "type": "TEXT",
                "data": {
                    "fromWxid": "test_user",
                    "toWxid": test_bot.gewe_app_id,
                    "content": "测试消息",
                    "msgId": "test_msg_id",
                },
            }

            print("模拟处理webhook消息...")
            result = await bot_manager.process_webhook_message(
                test_bot.gewe_app_id, mock_payload, session
            )

            if result:
                print("✅ 消息处理成功")
            else:
                print("❌ 消息处理失败")

    except Exception as e:
        print(f"消息处理测试失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_plugin_functionality())
    asyncio.run(test_message_processing())

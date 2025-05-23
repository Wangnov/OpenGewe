import aiohttp
from typing import Dict, Optional, Any, Literal, List
import asyncio
import qrcode
from functools import partial
import contextlib

from opengewe.modules.login import LoginModule
from opengewe.modules.message import MessageModule
from opengewe.modules.contact import ContactModule
from opengewe.modules.group import GroupModule
from opengewe.modules.tag import TagModule
from opengewe.modules.personal import PersonalModule
from opengewe.modules.favorite import FavoriteModule
from opengewe.modules.account import AccountModule
from opengewe.modules.sns import SnsModule
from opengewe.modules.finder import FinderModule
from opengewe.mixin import MessageMixin
from opengewe.callback.factory import MessageFactory
from opengewe.utils.plugin_manager import PluginManager
from opengewe.utils.decorators import scheduler
from opengewe.logger import get_logger

# 获取客户端日志记录器
logger = get_logger("GeweClient")


class GeweClient:
    """异步GeweAPI客户端

    Args:
        base_url: 调用Gewe服务的基础URL，通常为http://Gewe部署的镜像ip:2531/v2/api
        download_url: 从Gewe镜像中下载内容的URL，通常为http://Gewe部署的镜像ip:2532/download
        callback_url: 自行搭建的回调服务器URL，用于接收微信发来的回调消息
        app_id: 在Gewe镜像内登录的设备ID
        token: 登录token
        debug: 是否开启调试模式，默认关闭
        is_gewe: 是否使用付费版gewe，默认为False
        queue_type: 消息队列类型，"simple"或"advanced"，默认为"simple"
        queue_options: 消息队列选项，根据队列类型不同而不同，如高级队列需要broker、backend等参数
    """

    def __init__(
        self,
        base_url: str,
        download_url: str = "",
        callback_url: str = "",
        app_id: str = "",
        token: str = "",
        debug: bool = False,
        is_gewe: bool = False,
        queue_type: Literal["simple", "advanced"] = "simple",
        **queue_options: Any,
    ):
        self.base_url = base_url
        self.download_url = download_url
        self.callback_url = callback_url
        self.token = token
        self.app_id = app_id
        self.debug = debug
        # 登录过程中缓存的变量
        self.uuid: Optional[str] = None
        self.login_url: Optional[str] = None
        self.captch_code: Optional[str] = None
        # 判断是否为付费版gewe
        self.is_gewe = is_gewe or base_url == "http://www.geweapi.com/gewe/v2/api"

        # 创建HTTP会话
        self._session: Optional[aiohttp.ClientSession] = None

        # 初始化功能模块
        self.login = LoginModule(self)
        self.message = MessageModule(self)
        self.contact = ContactModule(self)
        self.group = GroupModule(self)
        self.tag = TagModule(self)
        self.personal = PersonalModule(self)
        self.favorite = FavoriteModule(self)
        self.account = AccountModule(self)
        self.sns = SnsModule(self)
        self.finder = FinderModule(self)

        # 创建并集成MessageMixin
        self._message_mixin = MessageMixin(self.message, queue_type, **queue_options)

        # 将MessageMixin的方法注册到Client实例
        self._register_message_methods()

        # 初始化插件管理器
        self.plugin_manager = PluginManager()
        self.plugin_manager.set_client(self)

        # 初始化消息工厂
        self.message_factory = MessageFactory(self)
        self.message_factory.set_plugin_manager(self.plugin_manager)

    def __str__(self) -> str:
        """返回客户端的字符串表示"""
        return (
            f"GeweClient(base_url={self.base_url}, "
            f"download_url={self.download_url}, "
            f"callback_url={self.callback_url}, "
            f"app_id={self.app_id}, "
            f"token={self.token[:4]}...{self.token[-4:] if len(self.token) > 8 else self.token})"
        )

    @property
    async def session(self) -> aiohttp.ClientSession:
        """获取或创建HTTP会话"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={"Content-Type": "application/json"}
            )
        return self._session

    def set_token(self, token: str) -> None:
        """设置API令牌"""
        self.token = token

    def set_app_id(self, app_id: str) -> None:
        """设置应用ID"""
        self.app_id = app_id

    async def request(
        self, endpoint: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """异步发送API请求

        Args:
            endpoint: API端点
            data: 请求数据

        Returns:
            Dict[str, Any]: API响应
        """
        headers = {"X-GEWE-TOKEN": self.token} if self.token else {}
        data = data or {}

        url = f"{self.base_url}{endpoint}"
        session = await self.session

        try:
            async with session.post(url, headers=headers, json=data) as response:
                # 尝试解析JSON响应
                try:
                    result = await response.json()
                except aiohttp.ContentTypeError:
                    # 处理非JSON响应
                    text = await response.text()
                    logger.error(f"API返回的非JSON响应: {text}")
                    return {"ret": 500, "msg": f"API返回的非JSON响应: {text[:100]}..."}

                # DEBUG用: 打印请求的url和请求体
                if self.debug:
                    logger.debug(f"请求的url: {url}")
                    logger.debug(f"请求的请求体: {data}")
                    logger.debug(f"请求的headers: {headers}")
                    logger.debug(f"请求的响应: {result}")

                # 检查HTTP状态码
                if response.status >= 400:
                    logger.error(f"HTTP错误: {response.status}, 响应: {result}")
                    return {
                        "ret": response.status,
                        "msg": f"HTTP错误 {response.status}: {result.get('msg', '未知错误')}",
                        "data": None,
                    }

                return result
        except aiohttp.ClientConnectorError as e:
            logger.error(f"❌ 连接错误: {e}")
            return {
                "ret": 500,
                "msg": f"无法连接到API服务器 {self.base_url}: {str(e)}",
                "data": None,
            }
        except aiohttp.ClientError as e:
            logger.error(f"❌ 请求网络错误: {e}")
            return {"ret": 500, "msg": f"网络请求异常: {str(e)}", "data": None}
        except asyncio.TimeoutError:
            logger.error("❌ 请求超时")
            return {"ret": 500, "msg": f"请求超时: {url}", "data": None}
        except Exception as e:
            logger.error(f"❌ 未知请求错误: {e}")
            return {"ret": 500, "msg": f"请求异常: {str(e)}", "data": None}

    async def close(self) -> None:
        """关闭客户端连接"""
        # 关闭调度器
        if scheduler.running:
            try:
                scheduler.shutdown()
                logger.debug("定时任务调度器已关闭")
            except Exception as e:
                logger.error(f"关闭调度器时出错: {e}")

        # 卸载插件
        if hasattr(self, "plugin_manager"):
            try:
                unloaded, failed = await self.plugin_manager.unload_plugins()
                if unloaded:
                    logger.info(f"已卸载 {len(unloaded)} 个插件: {', '.join(unloaded)}")
                if failed:
                    logger.warning(f"卸载失败的插件: {', '.join(failed)}")
            except Exception as e:
                logger.error(f"卸载插件时出错: {e}")

        # 关闭HTTP会话
        if self._session and not self._session.closed:
            with contextlib.suppress(Exception):
                await self._session.close()
                self._session = None

    async def __aenter__(self) -> "GeweClient":
        """异步上下文管理器入口"""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """异步上下文管理器退出"""
        await self.close()

    async def start_login(self) -> bool:
        """异步登录流程

        这是一个预先写好的异步终端登录流程，如在登录流程中出现问题，请自己执行login模块中的对应方法补全

        首次登录请将app_id和token传空以获取，之后登录请传入上一次登录返回的app_id和token

        Returns:
            bool: 登录是否成功
        """
        print("\n✨✨✨ 正在执行Gewe微信登录流程 ✨✨✨\n")

        # 检查登录设备，顺便查token可用性
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 📱 步骤 0: 检查登录设备并验证 Token 可用性        ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

        device_list_result, device_list_success = await self.login.get_device_list()
        token_available = False

        if device_list_success:
            print("✅ 获取登录设备的 appId 列表成功！Token 可用！")
            print("📋 已登录设备 app_id 列表: ")
            print(device_list_result)
            token_available = True
            if self.app_id and self.app_id not in device_list_result:
                print(
                    f'❌ 传入的 app_id: {self.app_id} 不在已登录设备的列表中\n   请传入正确的 app_id。如需登录新设备，请传入 app_id = ""'
                )
                return False
        else:
            msg = device_list_result.get("msg", "")
            if device_list_result.get("ret") == 500 and "不可用或已过期" in msg:
                print(
                    f"⚠️ 设置的 token: {self.token} 已过期或不可用，即将重新获取 token..."
                )
            elif (
                device_list_result.get("ret") == 500
                and "header:X-GEWE-TOKEN 不可为空" in msg
            ):
                print("⚠️ token 为空，即将重新获取 token...")
            else:
                print(device_list_result)
                return False

        # 获取token
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 🔑 步骤 1: 获取 Token                             ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

        if not token_available:
            token_result, token_success = await self.login.get_token()
            if token_success:
                print(f"✅ 获取新 token 成功！Token 已设置: {self.token}")
            else:
                print(token_result)
                return False
        else:
            print("✅ Token 可用，跳过获取 token")

        # 获取设备的appId和登录所需的uuid、登录二维码
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 📲 步骤 2: 获取设备的 appId、uuid 和登录二维码    ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

        qrcode_result, qrcode_success = await self.login.get_qrcode()
        if qrcode_success:
            print("✅ 获取二维码成功！")
            print(f"📱 app_id 已设置: {self.app_id}")
            print(f"🔑 uuid 已设置: {self.uuid}")
            print(f"🔗 登录链接: {self.login_url}")

            # 终端打印图片二维码
            try:
                # 使用事件循环的执行器运行阻塞的qrcode操作
                print("\n📱 请扫描下面的二维码登录: ")
                loop = asyncio.get_running_loop()
                qr_generator = partial(self._generate_qr_code, self.login_url)
                await loop.run_in_executor(None, qr_generator)
            except Exception as e:
                print(f"❌ 打印二维码时出错: {e}")
                print("⚠️ 请使用登录链接自行生成二维码后，使用微信扫描二维码登录")

            # 检测是否登录成功
            print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("┃ 🔄 步骤 3: 检测登录状态                           ┃")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

            max_retry = 60  # 最多检查60次，避免无限循环
            retry_count = 0

            while retry_count < max_retry:
                check_login_result = await self.login.check_login()
                login_data = check_login_result[0].get("data", {})

                if check_login_result[1]:
                    print("✅ 登录成功！")
                    break
                elif login_data.get("nickName") is not None:
                    print(
                        f"👤 已检测到微信用户: {login_data['nickName']} 扫码成功\n   请在手机上点击确认登录按钮...\n   ⏱️ 剩余操作时间: {login_data.get('expiredTime')}秒"
                    )
                    await asyncio.sleep(3)
                else:
                    if login_data.get("expiredTime") is None:
                        print("❌ 登录失败，执行登录超时！请重新执行登录流程")
                        return False
                    else:
                        print(
                            f"⏳ 等待扫码登录中... ⏱️ 剩余操作时间: {login_data.get('expiredTime')}秒"
                        )
                        await asyncio.sleep(3)

                retry_count += 1

            if retry_count >= max_retry:
                print("❌ 登录超时，请重新执行登录流程")
                return False
        else:
            data_msg = qrcode_result.get("data", {}).get("msg", "")
            if qrcode_result.get("ret") == 500:
                if qrcode_result.get("msg") == "微信已登录，请勿重复登录。":
                    print(f"⚠️ {qrcode_result.get('msg')}")
                    print("尝试设置回调服务器...")
                elif data_msg == "已达到最大客户端数量操作":
                    print(
                        "❌ 每个 token 只能登录两个 app_id（即使两个 app_id 是同一个微信）\n   请删除容器后重新创建容器，自动重置 token 后再进行操作"
                    )
                    return False
                else:
                    print(qrcode_result)
                    return False
            else:
                print(qrcode_result)
                return False

        # 设置回调
        print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃ 📡 步骤 4: 设置回调服务器                         ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

        callback_result, callback_success = await self.login.set_callback()
        if callback_success:
            print("✅ 设置回调成功")
            print(f"🔗 回调服务器: {self.callback_url}")
            print("\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
            print("┃ 🎉 登录流程结束，请妥善保管以下登录参数:          ┃")
            print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
            print(
                "{\n"
                + f"  'base_url': '{self.base_url}',\n"
                + f"  'download_url': '{self.download_url}',\n"
                + f"  'callback_url': '{self.callback_url}',\n"
                + f"  'app_id': '{self.app_id}',\n"
                + f"  'token': '{self.token}'\n"
                + "}"
            )
            return True
        else:
            print(f"❌ 设置回调失败: {callback_result}")
            return False

    def _generate_qr_code(self, url: str) -> None:
        """生成并打印二维码（同步方法，将在run_in_executor中调用）"""
        qr = qrcode.QRCode()
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)

    def _register_message_methods(self) -> None:
        """将MessageMixin的方法注册到Client实例"""
        # 获取MessageMixin的所有公开方法（不以下划线开头的方法）
        for method_name in dir(self._message_mixin):
            if not method_name.startswith("_"):
                method = getattr(self._message_mixin, method_name)
                if callable(method):
                    # 将方法注册到Client实例
                    setattr(self, method_name, method)

    async def start_plugins(self, plugins_directory: str = "plugins") -> List[str]:
        """启动插件系统

        Args:
            plugins_directory: 插件目录路径

        Returns:
            List[str]: 成功加载的插件名称列表
        """
        # 导入调度器模块
        from opengewe.utils.decorators import scheduler

        try:
            # 启动调度器
            if not scheduler.running:
                # 打印调度器状态
                logger.info(f"启动定时任务调度器。调度器时区: {scheduler.timezone}")
                scheduler.start()
                logger.info("定时任务调度器已启动成功")
            else:
                logger.info("定时任务调度器已在运行中")

            # 获取所有定时任务列表
            all_jobs = scheduler.get_jobs()
            if all_jobs:
                logger.info(f"当前已有 {len(all_jobs)} 个定时任务:")
                for job in all_jobs:
                    next_run = (
                        job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
                        if job.next_run_time
                        else "已暂停"
                    )
                    logger.info(f"  - 任务: {job.id}, 下次执行: {next_run}")
            else:
                logger.info("当前没有定时任务")

            # 加载插件
            logger.info(f"开始从 {plugins_directory} 加载插件...")
            loaded_plugins = await self.plugin_manager.load_plugins(plugins_directory)
            logger.info(
                f"已成功加载 {len(loaded_plugins)} 个插件: {', '.join(loaded_plugins)}"
            )

            # 再次检查定时任务
            all_jobs_after = scheduler.get_jobs()
            if all_jobs_after:
                logger.info(f"加载插件后，共有 {len(all_jobs_after)} 个定时任务:")
                for job in all_jobs_after:
                    next_run = (
                        job.next_run_time.strftime("%Y-%m-%d %H:%M:%S")
                        if job.next_run_time
                        else "已暂停"
                    )
                    logger.info(f"  - 任务: {job.id}, 下次执行: {next_run}")

            return loaded_plugins
        except Exception as e:
            logger.error(f"启动插件系统时出错: {e}", exc_info=True)
            return []

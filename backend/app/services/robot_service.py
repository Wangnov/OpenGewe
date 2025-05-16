"""机器人服务模块

提供微信机器人管理的业务逻辑，包括机器人的获取、状态管理、登录等功能。
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

from opengewe.logger import get_logger

from backend.app.models.robot import Robot
from backend.app.core.config import get_settings, DeviceSettings
from backend.app.gewe import client_manager, create_client, verify_client_config

# 获取日志记录器
logger = get_logger("RobotService")


class RobotService:
    """机器人服务类

    提供微信机器人管理的业务逻辑。
    """

    @staticmethod
    async def get_all_robots(include_inactive: bool = True) -> List[Dict[str, Any]]:
        """获取所有机器人

        Args:
            include_inactive: 是否包含非活跃的机器人

        Returns:
            List[Dict[str, Any]]: 机器人列表
        """
        if include_inactive:
            robots = await Robot.get_all()
        else:
            robots = await Robot.get_active()

        return [robot.to_dict() for robot in robots]

    @staticmethod
    async def get_robot_by_app_id(app_id: str) -> Optional[Dict[str, Any]]:
        """获取指定app_id的机器人

        Args:
            app_id: 机器人唯一ID

        Returns:
            Optional[Dict[str, Any]]: 机器人信息，如果不存在则为None
        """
        robot = await Robot.get_by_app_id(app_id)
        return robot.to_dict() if robot else None

    @staticmethod
    async def create_robot(
        app_id: str,
        token: str,
        name: Optional[str] = None,
        device_name: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """创建新机器人

        Args:
            app_id: 机器人唯一ID
            token: 微信登录token
            name: 机器人名称
            device_name: 设备名称
            config: 配置信息

        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: (是否成功, 消息, 机器人信息)
        """
        # 检查是否已存在
        existing = await Robot.get_by_app_id(app_id)
        if existing:
            return False, f"机器人 {app_id} 已存在", existing.to_dict()

        # 创建新机器人
        robot = await Robot.create(
            app_id=app_id,
            token=token,
            name=name,
            device_name=device_name,
            config=config,
        )

        if not robot:
            return False, f"创建机器人 {app_id} 失败", None

        # 同步到系统配置
        await RobotService._sync_robot_to_config(robot)

        return True, f"机器人 {app_id} 创建成功", robot.to_dict()

    @staticmethod
    async def update_robot_status(app_id: str, status: str) -> Tuple[bool, str]:
        """更新机器人状态

        Args:
            app_id: 机器人唯一ID
            status: 新状态

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = await Robot.update_status(app_id, status)
        if result:
            return True, f"机器人 {app_id} 状态已更新为 {status}"
        else:
            return False, f"机器人 {app_id} 不存在或状态更新失败"

    @staticmethod
    async def update_robot_profile(
        app_id: str,
        name: Optional[str] = None,
        wechat_id: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """更新机器人资料

        Args:
            app_id: 机器人唯一ID
            name: 新名称
            wechat_id: 新微信ID
            avatar_url: 新头像URL

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = await Robot.update_profile(
            app_id=app_id,
            name=name,
            wechat_id=wechat_id,
            avatar_url=avatar_url,
        )

        if result:
            # 获取更新后的机器人
            robot = await Robot.get_by_app_id(app_id)
            if robot:
                # 同步到系统配置
                await RobotService._sync_robot_to_config(robot)

            return True, f"机器人 {app_id} 资料已更新"
        else:
            return False, f"机器人 {app_id} 不存在或资料更新失败"

    @staticmethod
    async def activate_robot(app_id: str) -> Tuple[bool, str]:
        """激活机器人

        Args:
            app_id: 机器人唯一ID

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        result = await Robot.toggle_active(app_id, True)
        if result:
            return True, f"机器人 {app_id} 已激活"
        else:
            return False, f"机器人 {app_id} 不存在或激活失败"

    @staticmethod
    async def deactivate_robot(app_id: str) -> Tuple[bool, str]:
        """停用机器人

        Args:
            app_id: 机器人唯一ID

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        # 停用机器人
        result = await Robot.toggle_active(app_id, False)
        if not result:
            return False, f"机器人 {app_id} 不存在或停用失败"

        # 关闭客户端
        try:
            await client_manager.close_client(app_id)
        except Exception as e:
            logger.error(f"关闭机器人 {app_id} 客户端时出错: {e}")

        return True, f"机器人 {app_id} 已停用"

    @staticmethod
    async def delete_robot(app_id: str) -> Tuple[bool, str]:
        """删除机器人

        Args:
            app_id: 机器人唯一ID

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        # 先停用机器人
        await RobotService.deactivate_robot(app_id)

        # 删除机器人记录
        result = await Robot.delete_by_app_id(app_id)
        if result:
            # 从系统配置中移除
            await RobotService._remove_robot_from_config(app_id)

            return True, f"机器人 {app_id} 已删除"
        else:
            return False, f"机器人 {app_id} 不存在或删除失败"

    @staticmethod
    async def get_login_qrcode(
        app_id: str,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """获取登录二维码

        Args:
            app_id: 机器人唯一ID

        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: (是否成功, 消息, 二维码信息)
        """
        # 获取机器人信息
        robot = await Robot.get_by_app_id(app_id)
        if not robot:
            return False, f"机器人 {app_id} 不存在", None

        # 创建临时客户端
        try:
            device_config = DeviceSettings(
                name=robot.name or "临时机器人",
                base_url=robot.config_dict.get("base_url", ""),
                download_url=robot.config_dict.get("download_url", ""),
                callback_url=robot.config_dict.get("callback_url", ""),
                app_id=robot.app_id,
                token=robot.token,
                is_gewe=robot.config_dict.get("is_gewe", True),
            )

            client = await create_client(device_config=device_config)

            # 获取登录二维码
            result, success = await client.login.get_qrcode()
            await client.close()

            if success:
                # 更新机器人app_id和配置
                config = robot.config_dict
                config["uuid"] = result.get("uuid")
                config["login_url"] = result.get("qrData")

                await Robot.update_config(robot.app_id, config)

                qrcode_info = {
                    "qrData": result.get("qrData"),
                    "qrImgBase64": result.get("qrImgBase64"),
                    "uuid": result.get("uuid"),
                    "appId": result.get("appId"),
                }

                return True, "获取登录二维码成功", qrcode_info
            else:
                error_msg = result.get("msg", "未知错误")
                return False, f"获取登录二维码失败: {error_msg}", None

        except Exception as e:
            logger.error(f"获取机器人 {app_id} 登录二维码时出错: {e}")
            return False, f"获取登录二维码出错: {str(e)}", None

    @staticmethod
    async def check_login_status(
        app_id: str,
    ) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """检查登录状态

        Args:
            app_id: 机器人唯一ID

        Returns:
            Tuple[bool, str, Optional[Dict[str, Any]]]: (是否成功, 消息, 状态信息)
        """
        # 获取机器人信息
        robot = await Robot.get_by_app_id(app_id)
        if not robot:
            return False, f"机器人 {app_id} 不存在", None

        # 创建临时客户端
        try:
            config = robot.config_dict
            if not config.get("uuid"):
                return False, "缺少登录UUID，请先获取登录二维码", None

            device_config = DeviceSettings(
                name=robot.name or "临时机器人",
                base_url=config.get("base_url", ""),
                download_url=config.get("download_url", ""),
                callback_url=config.get("callback_url", ""),
                app_id=robot.app_id,
                token=robot.token,
                is_gewe=config.get("is_gewe", True),
            )

            client = await create_client(device_config=device_config)
            client.uuid = config.get("uuid")

            # 检查登录状态
            result, success = await client.login.check_login()

            # 如果登录成功，更新机器人信息
            if success and result.get("loginInfo"):
                login_info = result.get("loginInfo", {})

                # 更新机器人资料
                await Robot.update_profile(
                    app_id=robot.app_id,
                    name=login_info.get("nickName"),
                    wechat_id=login_info.get("wxid"),
                    avatar_url=login_info.get("headUrl"),
                )

                # 更新token和登录时间
                await Robot.update_token(robot.app_id, client.token)
                await Robot.update_status(robot.app_id, "online")

                # 更新登录时间
                from backend.app.db.session import DatabaseManager

                db_manager = DatabaseManager()
                async with db_manager.get_session() as session:
                    robot_obj = await Robot.get_by_app_id(robot.app_id)
                    robot_obj.login_time = datetime.now()
                    session.add(robot_obj)
                    await session.commit()

                # 同步到系统配置
                robot = await Robot.get_by_app_id(app_id)
                if robot:
                    await RobotService._sync_robot_to_config(robot)

                await client.close()

                return (
                    True,
                    "登录成功",
                    {
                        "status": "success",
                        "loginInfo": login_info,
                    },
                )

            # 如果是扫码状态
            elif result.get("nickName") is not None:
                await client.close()
                return (
                    True,
                    "已扫码，请在手机上确认登录",
                    {
                        "status": "scanned",
                        "nickname": result.get("nickName"),
                        "expiredTime": result.get("expiredTime"),
                    },
                )

            # 等待扫码状态
            else:
                await client.close()
                return (
                    True,
                    "等待扫码",
                    {
                        "status": "waiting",
                        "expiredTime": result.get("expiredTime"),
                    },
                )

        except Exception as e:
            logger.error(f"检查机器人 {app_id} 登录状态时出错: {e}")
            return False, f"检查登录状态出错: {str(e)}", None

    @staticmethod
    async def set_callback(app_id: str, callback_url: str) -> Tuple[bool, str]:
        """设置回调地址

        Args:
            app_id: 机器人唯一ID
            callback_url: 回调地址

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        # 获取机器人信息
        robot = await Robot.get_by_app_id(app_id)
        if not robot:
            return (
                False,
                f"机器人 {app_id} 不存在",
            )

        # 更新配置
        config = robot.config_dict
        config["callback_url"] = callback_url

        result = await Robot.update_config(app_id, config)
        if not result:
            return False, "更新回调地址失败"

        # 尝试设置回调
        try:
            # 创建临时客户端
            device_config = DeviceSettings(
                name=robot.name or "临时机器人",
                base_url=config.get("base_url", ""),
                download_url=config.get("download_url", ""),
                callback_url=callback_url,
                app_id=robot.app_id,
                token=robot.token,
                is_gewe=config.get("is_gewe", True),
            )

            client = await create_client(device_config=device_config)

            # 设置回调
            result, success = await client.login.set_callback()
            await client.close()

            if success:
                # 同步到系统配置
                robot = await Robot.get_by_app_id(app_id)
                if robot:
                    await RobotService._sync_robot_to_config(robot)

                return True, "设置回调地址成功"
            else:
                error_msg = result.get("msg", "未知错误")
                return False, f"设置回调地址失败: {error_msg}"

        except Exception as e:
            logger.error(f"设置机器人 {app_id} 回调地址时出错: {e}")
            return False, f"设置回调地址出错: {str(e)}"

    @staticmethod
    async def verify_robot_config(app_id: str) -> Tuple[bool, str]:
        """验证机器人配置

        Args:
            app_id: 机器人唯一ID

        Returns:
            Tuple[bool, str]: (是否成功, 消息)
        """
        # 获取机器人信息
        robot = await Robot.get_by_app_id(app_id)
        if not robot:
            return False, f"机器人 {app_id} 不存在"

        # 创建设备配置
        config = robot.config_dict
        device_config = DeviceSettings(
            name=robot.name or "临时机器人",
            base_url=config.get("base_url", ""),
            download_url=config.get("download_url", ""),
            callback_url=config.get("callback_url", ""),
            app_id=robot.app_id,
            token=robot.token,
            is_gewe=config.get("is_gewe", True),
        )

        # 验证配置
        is_valid, message = await verify_client_config(device_config=device_config)
        return is_valid, message

    @staticmethod
    async def _sync_robot_to_config(robot) -> None:
        """将机器人同步到系统配置

        Args:
            robot: 机器人对象
        """
        try:
            settings = get_settings()
            settings_dict = settings._config_data

            # 添加或更新设备配置
            if "devices" not in settings_dict:
                settings_dict["devices"] = {}

            config = robot.config_dict

            settings_dict["devices"][robot.app_id] = {
                "name": robot.name or f"机器人 {robot.app_id}",
                "base_url": config.get("base_url", ""),
                "download_url": config.get("download_url", ""),
                "callback_url": config.get("callback_url", ""),
                "app_id": robot.app_id,
                "token": robot.token,
                "is_gewe": config.get("is_gewe", True),
            }

            # 保存配置文件
            # TODO: 实现配置文件保存功能

        except Exception as e:
            logger.error(f"同步机器人 {robot.app_id} 到系统配置时出错: {e}")

    @staticmethod
    async def _remove_robot_from_config(app_id: str) -> None:
        """从系统配置中移除机器人

        Args:
            app_id: 机器人唯一ID
        """
        try:
            settings = get_settings()
            settings_dict = settings._config_data

            # 从设备配置中移除
            if "devices" in settings_dict and app_id in settings_dict["devices"]:
                del settings_dict["devices"][app_id]

            # 保存配置文件
            # TODO: 实现配置文件保存功能

        except Exception as e:
            logger.error(f"从系统配置中移除机器人 {app_id} 时出错: {e}")

    @staticmethod
    async def get_device_list() -> Tuple[bool, str, Optional[List[str]]]:
        """获取已登录设备列表

        Returns:
            Tuple[bool, str, Optional[List[str]]]: (是否成功, 消息, 设备列表)
        """
        try:
            # 获取默认客户端
            robot = await Robot.get_active()
            if not robot:
                return False, "没有活跃的机器人", None

            # 使用第一个活跃机器人
            first_robot = robot[0]

            # 创建临时客户端
            device_config = DeviceSettings(
                name=first_robot.name or "临时机器人",
                base_url=first_robot.config_dict.get("base_url", ""),
                download_url=first_robot.config_dict.get("download_url", ""),
                callback_url=first_robot.config_dict.get("callback_url", ""),
                app_id=first_robot.app_id,
                token=first_robot.token,
                is_gewe=first_robot.config_dict.get("is_gewe", True),
            )

            client = await create_client(device_config=device_config)

            # 获取设备列表
            result, success = await client.login.get_device_list()
            await client.close()

            if success:
                return True, "获取设备列表成功", result
            else:
                error_msg = result.get("msg", "未知错误")
                return False, f"获取设备列表失败: {error_msg}", None

        except Exception as e:
            logger.error(f"获取设备列表时出错: {e}")
            return False, f"获取设备列表出错: {str(e)}", None

from __future__ import annotations
from typing import (
    Dict,
    List,
    Any,
    Set,
    Optional,
    Type,
    Callable,
    Coroutine,
    Union,
    TYPE_CHECKING,
)
import json
import asyncio
import inspect

from opengewe.logger import get_logger
from opengewe.callback.types import MessageType
from opengewe.callback.models import (
    BaseMessage,
    TextMessage,
    ImageMessage,
    VoiceMessage,
    VideoMessage,
    EmojiMessage,
    LinkMessage,
    MiniappMessage,
    FileMessage,
    FileNoticeMessage,
    LocationMessage,
    CardMessage,
    FriendRequestMessage,
    GroupInviteMessage,
    GroupInvitedMessage,
    GroupRemovedMessage,
    GroupKickMessage,
    GroupDismissMessage,
    GroupRenameMessage,
    GroupOwnerChangeMessage,
    GroupInfoUpdateMessage,
    GroupAnnouncementMessage,
    GroupTodoMessage,
    GroupQuitMessage,
    RevokeMessage,
    PatMessage,
    OfflineMessage,
    SyncMessage,
    TransferMessage,
    RedPacketMessage,
    ContactUpdateMessage,
    ContactDeletedMessage,
    FinderMessage,
)
from opengewe.callback.handlers import DEFAULT_HANDLERS, BaseHandler

if TYPE_CHECKING:
    from opengewe.client import GeweClient
    from opengewe.utils.plugin_manager import PluginManager

# 获取消息工厂日志记录器
logger = get_logger("MessageFactory")

# 异步处理器类型定义
AsyncHandlerResult = Union[BaseMessage, None]
AsyncHandlerCoroutine = Coroutine[Any, Any, AsyncHandlerResult]
AsyncMessageCallback = Callable[[BaseMessage], Coroutine[Any, Any, Any]]


class MessageFactory:
    """消息工厂类，用于创建各种消息对象"""

    # 消息类型映射
    _message_type_map = {
        # 文本消息
        MessageType.TEXT: TextMessage,
        # 图片消息
        MessageType.IMAGE: ImageMessage,
        # 语音消息
        MessageType.VOICE: VoiceMessage,
        # 视频消息
        MessageType.VIDEO: VideoMessage,
        # 表情消息
        MessageType.EMOJI: EmojiMessage,
        # 链接消息
        MessageType.LINK: LinkMessage,
        # 小程序消息
        MessageType.MINIAPP: MiniappMessage,
        # 视频号消息
        MessageType.FINDER: FinderMessage,
        # 文件消息
        MessageType.FILE: FileMessage,
        # 文件通知消息
        MessageType.FILE_NOTICE: FileNoticeMessage,
        # 位置消息
        MessageType.LOCATION: LocationMessage,
        # 名片消息
        MessageType.CARD: CardMessage,
        # 引用消息
        MessageType.QUOTE: TextMessage,  # 临时使用TextMessage
        # 好友请求消息
        MessageType.FRIEND_REQUEST: FriendRequestMessage,
        # 联系人更新消息
        MessageType.CONTACT_UPDATE: ContactUpdateMessage,
        # 联系人删除消息
        MessageType.CONTACT_DELETED: ContactDeletedMessage,
        # 群聊邀请通知消息
        MessageType.GROUP_INVITE: GroupInviteMessage,
        # 被邀请入群通知消息
        MessageType.GROUP_INVITED: GroupInvitedMessage,
        # 被移出群聊消息
        MessageType.GROUP_REMOVED: GroupRemovedMessage,
        # 踢人消息
        MessageType.GROUP_KICK: GroupKickMessage,
        # 群解散消息
        MessageType.GROUP_DISMISS: GroupDismissMessage,
        # 修改群名称消息
        MessageType.GROUP_RENAME: GroupRenameMessage,
        # 群主变更消息
        MessageType.GROUP_OWNER_CHANGE: GroupOwnerChangeMessage,
        # 群信息变更消息
        MessageType.GROUP_INFO_UPDATE: GroupInfoUpdateMessage,
        # 群公告消息
        MessageType.GROUP_ANNOUNCEMENT: GroupAnnouncementMessage,
        # 群待办消息
        MessageType.GROUP_TODO: GroupTodoMessage,
        # 退出群聊消息
        MessageType.GROUP_QUIT: GroupQuitMessage,
        # 消息撤回
        MessageType.REVOKE: RevokeMessage,
        # 拍一拍消息
        MessageType.PAT: PatMessage,
        # 掉线消息
        MessageType.OFFLINE: OfflineMessage,
        # 同步消息
        MessageType.SYNC: SyncMessage,
        # 转账消息
        MessageType.TRANSFER: TransferMessage,
        # 红包消息
        MessageType.RED_PACKET: RedPacketMessage,
    }

    # MsgType到消息类型的映射（用于AddMsg类型消息）
    _msgtype_map = {
        1: MessageType.TEXT,        # 文本消息
        3: MessageType.IMAGE,       # 图片消息
        34: MessageType.VOICE,      # 语音消息
        42: MessageType.CARD,       # 名片消息
        43: MessageType.VIDEO,      # 视频消息
        47: MessageType.EMOJI,      # emoji表情
        48: MessageType.LOCATION,   # 地理位置
        49: MessageType.LINK,       # 公众号链接/小程序/文件/转账/红包/视频号等（需要进一步判断）
        37: MessageType.FRIEND_REQUEST,  # 好友请求
        10000: MessageType.TEXT,    # 系统文本消息（群操作等）
        10002: MessageType.REVOKE,  # 撤回/拍一拍/群公告/群待办等系统消息（需要进一步判断）
        51: MessageType.SYNC,       # 同步消息
    }

    # 添加TypeName到消息类型的映射
    _typename_map = {
        "ADDMSG": None,  # AddMsg需要通过MsgType进一步判断
        "MODCONTACTS": MessageType.CONTACT_UPDATE,
        "DELCONTACTS": MessageType.CONTACT_DELETED,
        "OFFLINE": MessageType.OFFLINE,
    }

    @classmethod
    async def create_message(
        cls, data: Dict[str, Any], client=None
    ) -> Optional[BaseMessage]:
        """创建消息对象

        Args:
            data: 原始消息数据
            client: GeweClient实例，用于下载图片等

        Returns:
            BaseMessage: 创建的消息对象，如果创建失败则返回None
        """
        # 判断是否包含消息数据
        if not data or not isinstance(data, dict):
            logger.error(f"无效的消息数据: {data}")
            return None

        try:
            # 尝试获取消息类型
            type_name = data.get("TypeName", "Unknown")
            type_name = type_name.upper()
            
            # 处理AddMsg类型消息，需要通过MsgType进一步判断
            if type_name == "ADDMSG":
                if "Data" not in data or "MsgType" not in data["Data"]:
                    logger.warning(f"AddMsg消息缺少MsgType字段: {data}")
                    return None
                
                msg_type = data["Data"]["MsgType"]
                message_type = cls._msgtype_map.get(msg_type)
                
                if message_type is None:
                    logger.warning(f"未知的MsgType: {msg_type}")
                    return None
                
                # 对于某些MsgType需要进一步判断具体类型
                if msg_type == 49:
                    # MsgType=49包括多种消息类型，需要进一步判断
                    content = data["Data"].get("Content", {}).get("string", "")
                    
                    # 检查是否是文件通知消息（type=74）
                    if "type>74</type" in content:
                        message_type = MessageType.FILE_NOTICE
                    # 检查是否是文件完成消息（type=6）
                    elif "type>6</type" in content and "appattach" in content:
                        message_type = MessageType.FILE
                    # 检查是否是小程序消息（type=33）
                    elif "type>33</type" in content:
                        message_type = MessageType.MINIAPP
                    # 检查是否是群邀请消息（type=5）
                    elif "type>5</type" in content:
                        message_type = MessageType.GROUP_INVITE
                    # 检查是否是视频号消息（finderFeed）
                    elif "finderFeed" in content:
                        message_type = MessageType.FINDER
                    # 检查是否是转账消息（type=2000）
                    elif "type>2000</type" in content or '<type><![CDATA[2000]]></type>' in content:
                        message_type = MessageType.TRANSFER
                    # 检查是否是红包消息（type=2001）
                    elif "type>2001</type" in content or '<type><![CDATA[2001]]></type>' in content:
                        message_type = MessageType.RED_PACKET
                    # 检查是否是引用消息（type=57）
                    elif "type>57</type" in content:
                        message_type = MessageType.QUOTE
                    # 默认为链接消息
                    else:
                        message_type = MessageType.LINK
                
                elif msg_type == 10002:
                    # MsgType=10002包括多种系统消息，需要进一步判断
                    content = data["Data"].get("Content", {}).get("string", "")
                    
                    # 检查是否是撤回消息
                    if "revokemsg" in content:
                        message_type = MessageType.REVOKE
                    # 检查是否是拍一拍消息
                    elif "type=\"pat\"" in content or '<sysmsg type="pat">' in content or 'type=\\"pat\\"' in content:
                        message_type = MessageType.PAT
                    # 检查是否是群公告消息
                    elif "mmchatroombarannouncememt" in content:
                        message_type = MessageType.GROUP_ANNOUNCEMENT
                    # 检查是否是群待办消息
                    elif "roomtoolstips" in content and "todo" in content:
                        message_type = MessageType.GROUP_TODO
                    # 检查是否是群解散消息（通过模板内容判断）
                    elif "已解散该群聊" in content:
                        message_type = MessageType.GROUP_DISMISS
                    # 检查是否是踢人消息（通过模板内容判断）
                    elif "移出了群聊" in content and "kickoutname" in content:
                        message_type = MessageType.GROUP_KICK
                    # 默认保持原类型
                    else:
                        message_type = MessageType.REVOKE
                
                elif msg_type == 10000:
                    # MsgType=10000主要是系统文本消息，需要根据内容判断具体类型
                    content = data["Data"].get("Content", {}).get("string", "")
                    
                    # 检查是否是群操作相关消息
                    if "你被" in content and "移出群聊" in content:
                        message_type = MessageType.GROUP_REMOVED
                    elif "移出了群聊" in content and "你将" not in content:
                        message_type = MessageType.GROUP_KICK
                    elif "解散该群聊" in content or ("群主" in content and "解散" in content):
                        message_type = MessageType.GROUP_DISMISS
                    elif "修改群名" in content:
                        message_type = MessageType.GROUP_RENAME
                    elif "成为新群主" in content:
                        message_type = MessageType.GROUP_OWNER_CHANGE
                    # 默认为文本消息
                    else:
                        message_type = MessageType.TEXT
                
                # 使用对应的消息类创建消息对象
                msg_cls = cls._message_type_map.get(message_type)
                if msg_cls:
                    logger.debug(f"通过MsgType {msg_type} 映射到消息类型 {message_type.name}")
                    return await msg_cls.from_dict(data, client)
            
            # 处理其他TypeName
            else:
                message_type = cls._typename_map.get(type_name)
                if message_type:
                    # 对于ModContacts，需要进一步判断是联系人更新还是群信息更新
                    if type_name == "MODCONTACTS" and "Data" in data:
                        username = data["Data"].get("UserName", {}).get("string", "")
                        if "@chatroom" in username:
                            message_type = MessageType.GROUP_INFO_UPDATE
                        else:
                            message_type = MessageType.CONTACT_UPDATE
                    
                    # 使用对应的消息类创建消息对象
                    msg_cls = cls._message_type_map.get(message_type)
                    if msg_cls:
                        logger.debug(f"通过TypeName '{type_name}' 映射到消息类型 {message_type.name}")
                        return await msg_cls.from_dict(data, client)
            
            # 如果没有找到对应的消息类型，返回None让处理器处理
            logger.debug(f"未找到TypeName '{type_name}' 的映射，将由处理器处理")
            return None
            
        except Exception as e:
            logger.error(f"创建消息对象失败: {e}", exc_info=True)
            return None

    def __init__(self, client: Optional["GeweClient"] = None):
        """初始化消息工厂

        Args:
            client: GeweClient实例，用于获取base_url和download_url，以便下载媒体文件
        """
        self.handlers: List[BaseHandler] = []
        self.client = client
        self.on_message_callback: Optional[AsyncMessageCallback] = None
        self._tasks: Set[asyncio.Task] = set()
        # 插件管理器将在后续步骤中实现
        self.plugin_manager: Optional["PluginManager"] = None

        # 注册默认的消息处理器
        for handler_cls in DEFAULT_HANDLERS:
            self.register_handler(handler_cls)

        logger.debug(f"消息工厂初始化完成，已注册 {len(self.handlers)} 个消息处理器")

    def register_handler(self, handler_cls: Type[BaseHandler]) -> None:
        """注册消息处理器

        Args:
            handler_cls: 处理器类，必须是BaseHandler的子类
        """
        if not issubclass(handler_cls, BaseHandler):
            raise TypeError(f"处理器必须是BaseHandler的子类，当前类型: {handler_cls}")

        handler = handler_cls(self.client)
        self.handlers.append(handler)

    def register_callback(self, callback: AsyncMessageCallback) -> None:
        """注册消息处理回调函数

        Args:
            callback: 异步回调函数，接收BaseMessage对象作为参数
        """
        self.on_message_callback = callback
        logger.debug(
            f"注册消息回调函数成功: {callback.__name__ if hasattr(callback, '__name__') else str(callback)}"
        )

    def set_plugin_manager(self, plugin_manager: "PluginManager") -> None:
        """设置插件管理器

        Args:
            plugin_manager: 插件管理器实例
        """
        self.plugin_manager = plugin_manager
        logger.debug("插件管理器设置成功")

    async def process(self, data: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理消息

        根据消息内容找到合适的处理器进行处理，返回处理后的消息对象。
        如果注册了回调函数，会在处理完成后调用回调函数。
        同时，会将消息传递给所有已启用的插件进行处理。

        Args:
            data: 原始消息数据，通常是从回调接口接收到的JSON数据

        Returns:
            处理后的消息对象，如果没有找到合适的处理器则返回None
        """
        # 尝试直接使用create_message方法创建消息对象
        type_name = data.get("TypeName", "未知")
        logger.debug(f"开始处理消息 TypeName={type_name}, Appid={data.get('Appid', '')}")

        # 首先尝试使用类映射直接创建消息对象
        message = await self.create_message(data, self.client)
        
        # 如果无法直接创建，则遍历处理器尝试处理
        if message is None:
            matched_handler = None
            for handler in self.handlers:
                try:
                    if await handler.can_handle(data):
                        matched_handler = handler.__class__.__name__
                        logger.debug(f"找到匹配的处理器: {matched_handler}")
                        message = await handler.handle(data)
                        if message:
                            logger.debug(
                                f"处理器 {matched_handler} 成功创建消息对象: {message.type.name}"
                            )
                        else:
                            logger.warning(f"处理器 {matched_handler} 返回了空消息对象")
                        break
                except Exception as e:
                    logger.error(
                        f"处理器 {handler.__class__.__name__} 处理消息时出错: {e}",
                        exc_info=True,
                    )

            if not matched_handler:
                logger.debug(f"没有找到匹配的处理器处理消息 TypeName={type_name}")

        # 如果没有找到合适的处理器，返回一个通用消息
        if message is None and data.get("TypeName") in [
            "AddMsg",
            "ModContacts",
            "DelContacts",
            "Offline",
        ]:
            message = BaseMessage(
                type=MessageType.UNKNOWN,
                app_id=data.get("Appid", ""),
                wxid=data.get("Wxid", ""),
                typename=data.get("TypeName", ""),
                raw_data=data,
            )
            logger.debug(f"创建了未知类型的通用消息对象: {type_name}")

        # 如果获取到了消息对象
        if message:
            # 如果注册了回调函数，创建任务异步调用回调函数
            if self.on_message_callback:
                logger.debug(f"准备调用消息回调函数处理 {message.type.name} 消息")
                task = asyncio.create_task(self._execute_callback(message))
                self._tasks.add(task)
                task.add_done_callback(self._tasks.discard)
            else:
                logger.debug("未注册消息回调函数，消息将不会被进一步处理")

            # 将消息传递给所有已启用的插件进行处理
            if self.plugin_manager:
                task = asyncio.create_task(self.plugin_manager.process_message(message))
                self._tasks.add(task)
                task.add_done_callback(self._tasks.discard)

        return message

    async def _execute_callback(self, message: BaseMessage) -> None:
        """异步执行回调函数

        Args:
            message: 处理后的消息对象
        """
        try:
            logger.debug(f"开始执行消息回调函数: {message.type.name}")
            await self.on_message_callback(message)
            logger.debug(f"消息回调函数执行完成: {message.type.name}")
        except Exception as e:
            logger.error(f"处理消息回调时出错: {e}", exc_info=True)

    async def process_json(self, json_data: str) -> Optional[BaseMessage]:
        """处理JSON格式的消息

        Args:
            json_data: JSON格式的消息数据

        Returns:
            处理后的消息对象，如果JSON解析失败或没有找到合适的处理器则返回None
        """
        try:
            data = json.loads(json_data)
            return await self.process(data)
        except json.JSONDecodeError:
            logger.error(f"JSON解析失败: {json_data}")
            return None
        except Exception as e:
            logger.error(f"处理消息时出错: {e}", exc_info=True)
            return None

    def process_async(self, data: Dict[str, Any]) -> asyncio.Task:
        """异步处理消息，不等待结果

        创建一个任务来处理消息，立即返回任务对象

        Args:
            data: 原始消息数据，通常是从回调接口接收到的JSON数据

        Returns:
            asyncio.Task: 消息处理任务
        """
        logger.debug(f"创建异步任务处理消息 TypeName={data.get('TypeName', '未知')}")
        task = asyncio.create_task(self.process(data))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    def process_json_async(self, json_data: str) -> asyncio.Task:
        """异步处理JSON格式的消息，不等待结果

        Args:
            json_data: JSON格式的消息数据

        Returns:
            asyncio.Task: 消息处理任务
        """
        task = asyncio.create_task(self.process_json(json_data))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    async def process_payload(self, payload: Dict[str, Any]) -> Optional[BaseMessage]:
        """处理回调payload，是process方法的别名

        用于处理webhook回调中的payload数据

        Args:
            payload: 原始消息数据，通常是从回调接口接收到的JSON数据

        Returns:
            处理后的消息对象，如果没有找到合适的处理器则返回None
        """
        return await self.process(payload)

    # 以下是插件系统相关方法，将在后续步骤中实现完整功能

    async def load_plugin(self, plugin_cls: Type) -> bool:
        """异步加载插件

        Args:
            plugin_cls: 插件类，必须是BasePlugin的子类

        Returns:
            是否成功加载插件
        """
        try:
            if self.plugin_manager:
                return await self.plugin_manager.register_plugin(plugin_cls)
            return False
        except Exception as e:
            logger.error(f"加载插件失败: {e}")
            return False

    async def load_plugins_from_directory(
        self, directory: str, prefix: str = ""
    ) -> List:
        """从目录异步加载插件

        Args:
            directory: 插件目录路径
            prefix: 模块前缀

        Returns:
            加载的插件列表
        """
        if self.plugin_manager:
            return await self.plugin_manager.load_plugins_from_directory(
                directory, prefix
            )
        return []

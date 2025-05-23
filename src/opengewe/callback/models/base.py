import time
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Type, TypeVar, ClassVar, TYPE_CHECKING
from opengewe.callback.types import MessageType
from opengewe.logger import get_logger

# 使用TYPE_CHECKING条件导入
if TYPE_CHECKING:
    from opengewe.client import GeweClient

# 消息类型变量，用于返回类型注解
T = TypeVar('T', bound='BaseMessage')
logger = get_logger("Callback")

@dataclass
class BaseMessage:
    """基础消息类"""

    type: MessageType  # 消息类型
    app_id: str  # 设备ID
    wxid: str = ""  # 所属微信ID
    typename: str = ""  # 原始消息类型名
    msg_id: str = ""  # 消息ID
    new_msg_id: str = ""  # 新消息ID
    create_time: int = 0  # 消息创建时间
    from_wxid: str = ""  # 来自哪个聊天的ID
    to_wxid: str = ""  # 接收者ID
    content: str = ""  # 消息内容
    sender_wxid: str = ""  # 实际发送者微信ID
    raw_data: Dict[str, Any] = field(default_factory=dict)  # 原始数据

    # 类变量，记录子类消息类型
    message_type: ClassVar[MessageType] = MessageType.UNKNOWN

    @property
    def is_group_message(self) -> bool:
        """判断是否为群聊消息"""
        # 检查from_wxid和to_wxid是否包含@chatroom
        if "@chatroom" in self.from_wxid or "@chatroom" in self.to_wxid:
            return True
        return False

    @property
    def is_self_message(self) -> bool:
        """判断是否为自己发送的消息"""
        if self.from_wxid == self.wxid:
            return True
        return False

    @property
    def datetime(self) -> str:
        """获取可读时间戳"""
        timearray = time.localtime(self.create_time)
        return time.strftime("%Y-%m-%d %H:%M:%S", timearray)

    def _process_group_message(self) -> None:
        """处理群消息发送者信息

        在群聊中：
        1. 保存群ID到room_wxid字段
        2. 识别真实发送者ID并更新from_wxid
        3. 去除content中的发送者前缀
        """
        # 如果不是群消息，写好sender_wxid后直接返回
        self.sender_wxid = self.from_wxid
        if not self.is_group_message:
            return

        # 处理content中的发送者信息
        if ":" in self.content:
            # 尝试分离发送者ID和实际内容
            parts = self.content.split(":", 1)
            if len(parts) == 2:
                sender_id = parts[0].strip()
                real_content = parts[1].strip()

                # 确保sender_id是一个有效的wxid格式（简单验证）
                if sender_id and (
                    sender_id.startswith("wxid_")
                    or sender_id.endswith("@chatroom")
                    or "@" in sender_id
                ):
                    # 更新发送者和内容
                    self.sender_wxid = sender_id
                    self.content = real_content
    
    @classmethod
    async def from_dict(cls: Type[T], data: Dict[str, Any], client: Optional["GeweClient"] = None) -> Optional[T]:
        """从字典创建消息对象
        
        Args:
            data: 原始数据
            client: GeweClient实例，用于下载媒体文件等
            
        Returns:
            消息对象，如果创建失败则返回None
        """
        try:
            # 创建基础消息对象
            msg = cls(
                type=cls.message_type,
                app_id=data.get("Appid", ""),
                wxid=data.get("Wxid", ""),
                typename=data.get("TypeName", ""),
                raw_data=data,
            )
            
            # 提取基础消息数据
            if "Data" in data:
                msg_data = data["Data"]
                msg.msg_id = str(msg_data.get("MsgId", ""))
                msg.new_msg_id = str(msg_data.get("NewMsgId", ""))
                msg.create_time = msg_data.get("CreateTime", 0)

                if "FromUserName" in msg_data and "string" in msg_data["FromUserName"]:
                    msg.from_wxid = msg_data["FromUserName"]["string"]

                if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                    msg.to_wxid = msg_data["ToUserName"]["string"]

                if "Content" in msg_data and "string" in msg_data["Content"]:
                    msg.content = msg_data["Content"]["string"]
                    
                    # 处理群消息发送者
                    msg._process_group_message()
                    
            # 调用子类特定的处理方法
            await msg._process_specific_data(data, client)
            
            return msg
        except Exception as e:
            logger.error(f"{cls.__name__}.from_dict处理失败: {e}", exc_info=True)
            return None
    
    async def _process_specific_data(self, data: Dict[str, Any], client: Optional["GeweClient"] = None) -> None:
        """处理特定消息类型的数据，子类应重写此方法
        
        Args:
            data: 原始数据
            client: GeweClient实例，用于下载媒体文件等
        """
        # 基类不做任何处理，由子类重写
        pass

# 中间抽象类

@dataclass
class MediaBaseMessage(BaseMessage):
    """媒体消息基类，用于图片、语音、视频等媒体类消息"""
    
    async def _download_media(self, client: Optional["GeweClient"], download_method, content: str, **kwargs) -> Optional[str]:
        """通用媒体下载方法
        
        Args:
            client: GeweClient实例
            download_method: 客户端下载方法
            content: 消息内容
            **kwargs: 其他参数
            
        Returns:
            下载URL，如果下载失败则返回None
        """
        if not client or not content:
            return None
            
        try:
            download_result = await download_method(content, **kwargs)
            if (download_result and 
                download_result.get("ret") == 200 and 
                "data" in download_result):
                file_url = download_result["data"].get("fileUrl", "")
                if file_url and client.download_url:
                    return f"{client.download_url}?url={file_url}"
        except Exception as e:
            logger.debug(f"媒体下载失败: {e}")
        
        return None

@dataclass
class TextBaseMessage(BaseMessage):
    """文本类消息基类，用于纯文本和引用消息等"""
    text: str = ""  # 文本内容

@dataclass
class FileBaseMessage(BaseMessage):
    """文件消息基类，用于文件和文件通知消息"""
    file_name: str = ""  # 文件名
    file_ext: str = ""  # 文件扩展名
    file_size: int = 0  # 文件大小 

@dataclass
class GroupBaseMessage(BaseMessage):
    """群聊相关消息基类"""
    group_id: str = ""  # 群聊ID
    group_name: str = ""  # 群聊名称

@dataclass 
class ContactBaseMessage(BaseMessage):
    """联系人相关消息基类"""
    nickname: str = ""  # 昵称

@dataclass
class SystemBaseMessage(BaseMessage):
    """系统消息基类"""
    pass

@dataclass
class PaymentBaseMessage(BaseMessage):
    """支付相关消息基类"""
    pass

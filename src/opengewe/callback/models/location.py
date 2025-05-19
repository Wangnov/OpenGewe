from dataclasses import dataclass
from typing import Dict, Any
import xml.etree.ElementTree as ET

from opengewe.callback.types import MessageType
from opengewe.callback.models.base import BaseMessage


@dataclass
class LocationMessage(BaseMessage):
    """位置消息"""

    latitude: float = 0.0  # 纬度
    longitude: float = 0.0  # 经度
    label: str = ""  # 位置名称
    scale: int = 16  # 地图缩放等级
    pointer_url: str = ""  # 位置图标URL

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LocationMessage":
        """从字典创建位置消息对象"""
        msg = cls(
            type=MessageType.LOCATION,
            app_id=data.get("Appid", ""),
            wxid=data.get("Wxid", ""),
            typename=data.get("TypeName", ""),
            raw_data=data,
        )

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

                # 解析XML获取位置信息
                try:
                    root = ET.fromstring(msg.content)

                    # 先尝试解析新版位置消息
                    location = root.find("location")
                    if location is not None:
                        try:
                            msg.latitude = float(location.get("x", "0.0"))
                            msg.longitude = float(location.get("y", "0.0"))
                        except ValueError:
                            pass

                        msg.label = location.get("label", "")
                        try:
                            msg.scale = int(location.get("scale", "16"))
                        except ValueError:
                            pass

                        msg.pointer_url = location.get("poiname", "")

                    # 再尝试解析appMsg格式的位置消息
                    else:
                        appmsg = root.find("appmsg")
                        if appmsg is not None:
                            location_info = appmsg.find("location_info")
                            if location_info is not None:
                                try:
                                    msg.latitude = float(location_info.get("x", "0.0"))
                                    msg.longitude = float(location_info.get("y", "0.0"))
                                except ValueError:
                                    pass

                                msg.label = location_info.get("label", "")

                                try:
                                    msg.scale = int(location_info.get("scale", "16"))
                                except ValueError:
                                    pass

                                msg.pointer_url = location_info.get("poiname", "")
                except Exception:
                    pass

        return msg

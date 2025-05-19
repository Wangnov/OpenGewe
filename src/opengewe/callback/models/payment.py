from dataclasses import dataclass
from typing import Dict, Any, Optional
import xml.etree.ElementTree as ET

from opengewe.callback.types import MessageType
from opengewe.callback.models.base import BaseMessage


@dataclass
class TransferMessage(BaseMessage):
    """转账消息"""

    amount: float = 0.0  # 转账金额（元）
    trans_id: str = ""  # 转账ID
    trans_time: int = 0  # 转账时间戳
    description: str = ""  # 转账说明
    status: str = ""  # 转账状态
    sender_wxid: str = ""  # 转账发送者wxid
    receiver_wxid: str = ""  # 转账接收者wxid

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TransferMessage":
        """从字典创建转账消息对象"""
        msg = cls(
            type=MessageType.TRANSFER,
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
                msg.sender_wxid = msg.from_wxid

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]
                msg.receiver_wxid = msg.to_wxid

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 处理群消息发送者
                msg._process_group_message()

                # 解析XML获取转账信息
                try:
                    root = ET.fromstring(msg.content)
                    msg_node = root.find("appmsg")
                    if msg_node is not None:
                        # 确认消息类型是否为转账
                        type_node = msg_node.find("type")
                        if (
                            type_node is not None
                            and type_node.text
                            and type_node.text == "2000"
                        ):
                            # 获取转账详情
                            wcpay_info = msg_node.find("wcpayinfo")
                            if wcpay_info is not None:
                                # 获取转账金额（单位为分，需要转换为元）
                                fee_node = wcpay_info.find("feedesc")
                                if fee_node is not None and fee_node.text:
                                    # 特殊处理金额，去除¥符号等，然后转换为浮点数
                                    try:
                                        amount_str = fee_node.text.replace(
                                            "¥", ""
                                        ).strip()
                                        msg.amount = float(amount_str)
                                    except ValueError:
                                        pass

                                # 获取转账ID
                                trans_id_node = wcpay_info.find("transferid")
                                if trans_id_node is not None and trans_id_node.text:
                                    msg.trans_id = trans_id_node.text

                                # 获取转账说明
                                desc_node = wcpay_info.find("pay_memo")
                                if desc_node is not None and desc_node.text:
                                    msg.description = desc_node.text

                                # 获取转账状态
                                status_node = wcpay_info.find("overduetime")
                                if status_node is not None:
                                    # 如果有过期时间，说明转账还未被领取
                                    msg.status = "waiting"
                                else:
                                    # 否则说明已经被领取或已退回
                                    msg.status = "received"

                                # 获取转账时间
                                time_node = wcpay_info.find("transcationtime")
                                if time_node is not None and time_node.text:
                                    try:
                                        msg.trans_time = int(time_node.text)
                                    except ValueError:
                                        pass
                except Exception:
                    pass

        return msg


@dataclass
class RedPacketMessage(BaseMessage):
    """红包消息"""

    amount: float = 0.0  # 红包金额（如果已知）（元）
    packet_id: str = ""  # 红包ID
    desc: str = ""  # 红包描述/祝福语
    sender_wxid: str = ""  # 红包发送者wxid
    sender_nickname: str = ""  # 红包发送者昵称
    packet_type: str = ""  # 红包类型(个人红包/群红包/拼手气红包)
    wishing: str = ""  # 祝福语
    status: str = ""  # 红包状态(未领取/已领取/已过期)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RedPacketMessage":
        """从字典创建红包消息对象"""
        msg = cls(
            type=MessageType.RED_PACKET,
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
                msg.sender_wxid = msg.from_wxid

            if "ToUserName" in msg_data and "string" in msg_data["ToUserName"]:
                msg.to_wxid = msg_data["ToUserName"]["string"]

            if "Content" in msg_data and "string" in msg_data["Content"]:
                msg.content = msg_data["Content"]["string"]

                # 解析XML获取红包信息
                try:
                    root = ET.fromstring(msg.content)
                    msg_node = root.find("appmsg")
                    if msg_node is not None:
                        # 确认消息类型是否为红包
                        type_node = msg_node.find("type")
                        if (
                            type_node is not None
                            and type_node.text
                            and type_node.text == "2001"
                        ):
                            # 获取红包类型和祝福语
                            wcpay_info = msg_node.find("wcpayinfo")
                            if wcpay_info is not None:
                                # 获取红包描述
                                desc_node = wcpay_info.find("sendertitle")
                                if desc_node is not None and desc_node.text:
                                    msg.desc = desc_node.text

                                # 获取红包ID
                                packet_id_node = wcpay_info.find("receivertitle")
                                if packet_id_node is not None and packet_id_node.text:
                                    msg.packet_id = packet_id_node.text

                                # 获取祝福语
                                wishing_node = wcpay_info.find("innertype")
                                if wishing_node is not None and wishing_node.text:
                                    msg.wishing = wishing_node.text

                                # 获取红包发送者昵称
                                nickname_node = wcpay_info.find("sendusername")
                                if nickname_node is not None and nickname_node.text:
                                    msg.sender_nickname = nickname_node.text

                                # 判断红包类型
                                if "@chatroom" in msg.to_wxid:
                                    # 群红包
                                    is_exclusive_node = wcpay_info.find("is_exclusive")
                                    if (
                                        is_exclusive_node is not None
                                        and is_exclusive_node.text == "1"
                                    ):
                                        # 专属红包
                                        msg.packet_type = "exclusive_group"
                                    else:
                                        # 拼手气红包
                                        msg.packet_type = "lucky_group"
                                else:
                                    # 个人红包
                                    msg.packet_type = "personal"

                                # 判断红包状态
                                status_node = wcpay_info.find("status")
                                if status_node is not None and status_node.text:
                                    if status_node.text == "2":
                                        msg.status = "received"
                                    elif status_node.text == "3":
                                        msg.status = "expired"
                                    else:
                                        msg.status = "waiting"
                except Exception:
                    pass

        return msg

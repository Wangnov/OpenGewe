from typing import Dict
import requests


class MessageModule:
    """消息模块"""

    def __init__(self, client):
        self.client = client

    def download_image(self, msg_id: str) -> Dict:
        """下载图片"""
        data = {"msgId": msg_id}
        headers = {"X-GEWE-TOKEN": self.client.token} if self.client.token else {}
        headers["Content-Type"] = "application/json"

        url = f"{self.client.download_url}/message/downloadImage"
        response = requests.post(url, headers=headers, json=data)

        return response.json()

    def send_text(self, to_wxid: str, content: str) -> Dict:
        """发送文字消息"""
        data = {"toWxid": to_wxid, "content": content}
        return self.client.request("/message/sendText", data)

    def send_file(self, to_wxid: str, file_path: str) -> Dict:
        """发送文件消息"""
        data = {"toWxid": to_wxid, "filePath": file_path}
        return self.client.request("/message/sendFile", data)

    def send_image(self, to_wxid: str, image_path: str) -> Dict:
        """发送图片消息"""
        data = {"toWxid": to_wxid, "imagePath": image_path}
        return self.client.request("/message/sendImage", data)

    def send_voice(self, to_wxid: str, voice_path: str) -> Dict:
        """发送语音消息"""
        data = {"toWxid": to_wxid, "voicePath": voice_path}
        return self.client.request("/message/sendVoice", data)

    def send_video(self, to_wxid: str, video_path: str) -> Dict:
        """发送视频消息"""
        data = {"toWxid": to_wxid, "videoPath": video_path}
        return self.client.request("/message/sendVideo", data)

    def send_link(
        self, to_wxid: str, title: str, desc: str, url: str, image_url: str = ""
    ) -> Dict:
        """发送链接消息"""
        data = {
            "toWxid": to_wxid,
            "title": title,
            "desc": desc,
            "url": url,
            "imageUrl": image_url,
        }
        return self.client.request("/message/sendLink", data)

    def send_card(self, to_wxid: str, card_wxid: str) -> Dict:
        """发送名片消息"""
        data = {"toWxid": to_wxid, "cardWxid": card_wxid}
        return self.client.request("/message/sendCard", data)

    def send_emoji(self, to_wxid: str, emoji_path: str) -> Dict:
        """发送emoji消息"""
        data = {"toWxid": to_wxid, "emojiPath": emoji_path}
        return self.client.request("/message/sendEmoji", data)

    def send_appmsg(self, to_wxid: str, app_msg: Dict) -> Dict:
        """发送appmsg消息"""
        data = {"toWxid": to_wxid, "appMsg": app_msg}
        return self.client.request("/message/sendAppMsg", data)

    def send_miniprogram(self, to_wxid: str, mini_program: Dict) -> Dict:
        """发送小程序消息"""
        data = {"toWxid": to_wxid, "miniProgram": mini_program}
        return self.client.request("/message/sendMiniProgram", data)

    def forward_file(self, to_wxid: str, msg_id: str) -> Dict:
        """转发文件"""
        data = {"toWxid": to_wxid, "msgId": msg_id}
        return self.client.request("/message/forwardFile", data)

    def forward_image(self, to_wxid: str, msg_id: str) -> Dict:
        """转发图片"""
        data = {"toWxid": to_wxid, "msgId": msg_id}
        return self.client.request("/message/forwardImage", data)

    def forward_video(self, to_wxid: str, msg_id: str) -> Dict:
        """转发视频"""
        data = {"toWxid": to_wxid, "msgId": msg_id}
        return self.client.request("/message/forwardVideo", data)

    def forward_link(self, to_wxid: str, msg_id: str) -> Dict:
        """转发链接"""
        data = {"toWxid": to_wxid, "msgId": msg_id}
        return self.client.request("/message/forwardLink", data)

    def forward_miniprogram(self, to_wxid: str, msg_id: str) -> Dict:
        """转发小程序"""
        data = {"toWxid": to_wxid, "msgId": msg_id}
        return self.client.request("/message/forwardMiniProgram", data)

    def revoke_message(self, msg_id: str) -> Dict:
        """撤回消息"""
        data = {"msgId": msg_id}
        return self.client.request("/message/revoke", data)

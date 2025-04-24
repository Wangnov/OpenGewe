from typing import Dict, List


class TagModule:
    """标签模块"""

    def __init__(self, client):
        self.client = client

    def add_tag(self, label_name: str) -> Dict:
        """添加标签

        Summary:
            标签名称不存在则是添加标签，如果标签名称已经存在，此接口会直接返回标签名及ID

        Args:
            label_name (str): 标签名称

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "labelName": str,  # 标签名称
                        "labelId": int  # 标签ID
                    }
                }
        """
        data = {"appId": self.client.app_id, "labelName": label_name}
        return self.client.request("/label/add", data)

    def delete_tag(self, label_ids: str) -> Dict:
        """删除标签

        Args:
            label_ids (str): 标签ID，多个以逗号分隔

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str  # 返回信息
                }
        """
        data = {"appId": self.client.app_id, "labelIds": label_ids}
        return self.client.request("/label/delete", data)

    def get_tags(self) -> Dict:
        """获取标签列表

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str,  # 返回信息
                    "data": {
                        "labelList": [
                            {
                                "labelName": str,  # 标签名称
                                "labelId": int  # 标签ID
                            }
                        ]
                    }
                }
        """
        data = {"appId": self.client.app_id}
        return self.client.request("/label/list", data)

    def modify_friend_tags(self, wx_ids: List[str], label_ids: str) -> Dict:
        """修改好友标签

        Summary:
            由于好友标签信息存储在用户客户端，因此每次在修改时都需要进行全量修改。
            例如：好友A（wxid_123）已有标签ID为1和2，
            添加标签ID为3时，需传参：label_ids="1,2,3"，wx_ids=["wxid_123"]
            删除标签ID为1时，需传参：label_ids="2,3"，wx_ids=["wxid_123"]

        Args:
            wx_ids (List[str]): 要修改标签的好友wxid列表
            label_ids (str): 标签ID，多个以逗号分隔

        Returns:
            Dict: Gewechat返回结果，格式如下:
                {
                    "ret": int,  # 返回码，200表示成功
                    "msg": str  # 返回信息
                }
        """
        data = {"appId": self.client.app_id, "wxIds": wx_ids, "labelIds": label_ids}
        return self.client.request("/label/modifyMemberList", data)

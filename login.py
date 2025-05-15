from opengewe.client import GeweClient


def main():
    # 配置参数
    base_url = "http://localhost:2531/v2/api"
    download_url = "http://localhost:2532/download"
    callback_url = "http://ip:5432/callback"
    app_id = ""
    token = ""
    # 创建 GewechatClient 实例
    client = GeweClient(
        base_url,
        download_url,
        callback_url,
        app_id,
        token,
    )
    # client.debug = True
    client.start_login()


if __name__ == "__main__":
    main()

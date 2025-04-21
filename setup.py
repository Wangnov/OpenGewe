from setuptools import setup, find_packages

setup(
    name="opengewechat",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "typing>=3.7.4",
    ],
    author="OpenGewechat",
    author_email="contact@example.com",
    description="Python客户端用于Gewechat API",
    keywords="wechat, api, client",
    python_requires=">=3.6",
)

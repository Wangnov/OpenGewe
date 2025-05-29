"""
代理服务相关API路由
"""

import httpx
import base64
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.session_manager import get_admin_session
from ..core.security import get_current_active_user
from opengewe.logger import init_default_logger, get_logger

init_default_logger()
logger = get_logger(__name__)

router = APIRouter()

# 允许代理的域名白名单
ALLOWED_DOMAINS = [
    "shmmsns.qpic.cn",
    "mmsns.qpic.cn", 
    "wx.qlogo.cn",
    "thirdwx.qlogo.cn",
    "weixin.qq.com",
    "res.wx.qq.com"
]


def is_allowed_domain(url: str) -> bool:
    """检查URL是否在允许的域名白名单中"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        return any(allowed in domain for allowed in ALLOWED_DOMAINS)
    except Exception:
        return False


@router.get("/image", summary="代理微信图片")
async def proxy_wechat_image(
    url: str = Query(..., description="要代理的图片URL"),
    current_user: dict = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session),
):
    """
    代理微信图片请求
    
    解决微信图片防盗链问题，通过后端代理转发图片请求
    """
    # 验证URL是否在允许的域名白名单中
    if not is_allowed_domain(url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不允许代理此域名的图片"
        )
    
    try:
        # 使用httpx客户端请求图片
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(10.0),
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Referer": "https://wx.qq.com/",
                "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            }
        ) as client:
            response = await client.get(url)
            
            if response.status_code != 200:
                logger.warning(f"图片代理请求失败: {url}, 状态码: {response.status_code}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="图片不存在或无法访问"
                )
            
            # 检查内容类型
            content_type = response.headers.get("content-type", "")
            if not content_type.startswith("image/"):
                logger.warning(f"非图片内容类型: {url}, content-type: {content_type}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="URL内容不是图片"
                )
            
            # 返回图片数据
            return Response(
                content=response.content,
                media_type=content_type,
                headers={
                    "Cache-Control": "public, max-age=3600",  # 缓存1小时
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Access-Control-Allow-Headers": "*",
                }
            )
            
    except httpx.TimeoutException:
        logger.error(f"图片代理请求超时: {url}")
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="请求图片超时"
        )
    except httpx.RequestError as e:
        logger.error(f"图片代理请求错误: {url}, 错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="代理请求失败"
        )
    except Exception as e:
        logger.error(f"图片代理未知错误: {url}, 错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="代理服务器内部错误"
        )


@router.get("/image/base64", summary="获取base64编码的图片")
async def get_image_base64(
    url: str = Query(..., description="要获取的图片URL"),
    current_user: dict = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session),
):
    """
    获取base64编码的图片数据
    
    返回JSON格式的base64数据，适用于需要内嵌图片的场景
    """
    # 验证URL是否在允许的域名白名单中
    if not is_allowed_domain(url):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不允许代理此域名的图片"
        )
    
    try:
        # 使用httpx客户端请求图片
        async with httpx.AsyncClient(
            timeout=httpx.Timeout(10.0),
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Referer": "https://wx.qq.com/",
                "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Cache-Control": "no-cache",
                "Pragma": "no-cache",
            }
        ) as client:
            response = await client.get(url)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="图片不存在或无法访问"
                )
            
            # 检查内容类型
            content_type = response.headers.get("content-type", "")
            if not content_type.startswith("image/"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="URL内容不是图片"
                )
            
            # 编码为base64
            base64_data = base64.b64encode(response.content).decode('utf-8')
            
            return {
                "success": True,
                "data": f"data:{content_type};base64,{base64_data}",
                "content_type": content_type,
                "size": len(response.content)
            }
            
    except httpx.TimeoutException:
        logger.error(f"图片代理请求超时: {url}")
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail="请求图片超时"
        )
    except httpx.RequestError as e:
        logger.error(f"图片代理请求错误: {url}, 错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="代理请求失败"
        )
    except Exception as e:
        logger.error(f"图片代理未知错误: {url}, 错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="代理服务器内部错误"
        ) 
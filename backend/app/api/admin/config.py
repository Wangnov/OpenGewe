"""
配置管理API端点
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...core.database import get_admin_session
from ...core.security import get_current_active_user
from ...models.admin import Admin
from ...services.config_manager import config_manager
from ...services.initializers.config_initializer import config_initializer
from ...schemas.config import (
    ConfigSectionResponse,
    ConfigUpdateRequest,
    ConfigMigrationStatus,
    AllConfigsResponse,
)

router = APIRouter()


async def get_current_admin(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_admin_session),
) -> Admin:
    """获取当前管理员用户"""
    user_id = current_user.get("id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户信息无效"
        )

    stmt = select(Admin).where(Admin.id == int(user_id))
    result = await session.execute(stmt)
    admin = result.scalar_one_or_none()

    if not admin or not admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="管理员账户不存在或已被禁用",
        )

    return admin


@router.get("", response_model=AllConfigsResponse)
async def get_all_configs(current_admin: Admin = Depends(get_current_admin)):
    """
    获取所有配置段

    需要管理员权限
    """
    try:
        configs = await config_manager.get_all_configs()

        return AllConfigsResponse(
            status="success", data=configs, message=f"成功获取 {len(configs)} 个配置段"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取配置失败: {str(e)}",
        )


@router.get("/{section_name}", response_model=ConfigSectionResponse)
async def get_config_section(
    section_name: str, current_admin: Admin = Depends(get_current_admin)
):
    """
    获取指定配置段

    需要管理员权限
    """
    if section_name == "gewe_apps":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="gewe_apps配置段不支持通过此API访问，请使用专门的机器人管理API",
        )

    try:
        config_data = await config_manager.get_config(section_name)

        if config_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"配置段不存在: {section_name}",
            )

        return ConfigSectionResponse(
            status="success",
            data={"section_name": section_name, "config": config_data},
            message=f"成功获取配置段: {section_name}",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取配置段失败: {str(e)}",
        )


@router.put("/{section_name}", response_model=ConfigSectionResponse)
async def update_config_section(
    section_name: str,
    request: ConfigUpdateRequest,
    current_admin: Admin = Depends(get_current_admin),
):
    """
    更新指定配置段

    需要管理员权限
    """
    # 检查是否是受保护的配置段
    if section_name == "gewe_apps":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="gewe_apps配置段不支持通过此API修改，请使用专门的机器人管理API",
        )

    # 检查是否是支持的配置段
    if section_name not in config_initializer.MIGRATE_SECTIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的配置段: {section_name}。支持的配置段: {config_initializer.MIGRATE_SECTIONS}",
        )

    try:
        # 验证配置数据（根据配置段类型进行基础验证）
        validation_result = _validate_config_data(section_name, request.config)
        if not validation_result["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"配置验证失败: {validation_result['error']}",
            )

        # 更新配置
        success = await config_manager.set_config(section_name, request.config)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="配置更新失败"
            )

        return ConfigSectionResponse(
            status="success",
            data={"section_name": section_name, "config": request.config},
            message=f"成功更新配置段: {section_name}",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新配置段失败: {str(e)}",
        )


@router.delete("/{section_name}")
async def delete_config_section(
    section_name: str, current_admin: Admin = Depends(get_current_admin)
):
    """
    删除指定配置段

    需要管理员权限
    """
    # 检查是否是受保护的配置段
    if section_name == "gewe_apps":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="gewe_apps配置段不允许删除"
        )

    try:
        success = await config_manager.delete_config(section_name)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"配置段不存在: {section_name}",
            )

        return {"status": "success", "message": f"成功删除配置段: {section_name}"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除配置段失败: {str(e)}",
        )


@router.post("/migrate", response_model=ConfigMigrationStatus)
async def trigger_config_migration(current_admin: Admin = Depends(get_current_admin)):
    """
    触发配置迁移

    将TOML文件中的配置迁移到数据库
    需要管理员权限
    """
    try:
        success = await config_initializer.initialize_config()
        status_info = await config_initializer.get_migration_status()

        return ConfigMigrationStatus(
            status="success" if success else "partial_success",
            data=status_info,
            message="配置迁移完成" if success else "配置迁移部分完成",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"配置迁移失败: {str(e)}",
        )


@router.get("/migration/status", response_model=ConfigMigrationStatus)
async def get_migration_status(current_admin: Admin = Depends(get_current_admin)):
    """
    获取配置迁移状态

    需要管理员权限
    """
    try:
        status_info = await config_initializer.get_migration_status()

        return ConfigMigrationStatus(
            status="success", data=status_info, message="成功获取迁移状态"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取迁移状态失败: {str(e)}",
        )


@router.post("/cache/clear")
async def clear_config_cache(
    section_name: str = None, current_admin: Admin = Depends(get_current_admin)
):
    """
    清除配置缓存

    需要管理员权限
    """
    try:
        config_manager.clear_cache(section_name)

        message = (
            f"成功清除配置段缓存: {section_name}"
            if section_name
            else "成功清除所有配置缓存"
        )

        return {"status": "success", "message": message}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"清除缓存失败: {str(e)}",
        )


@router.get("/cache/status")
async def get_cache_status(current_admin: Admin = Depends(get_current_admin)):
    """
    获取配置缓存状态

    需要管理员权限
    """
    try:
        cache_status = config_manager.get_cache_status()

        return {
            "status": "success",
            "data": cache_status,
            "message": "成功获取缓存状态",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取缓存状态失败: {str(e)}",
        )


def _validate_config_data(
    section_name: str, config_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    验证配置数据的基础结构

    Args:
        section_name: 配置段名称
        config_data: 配置数据

    Returns:
        验证结果
    """
    try:
        if not isinstance(config_data, dict):
            return {"valid": False, "error": "配置数据必须是字典格式"}

        # 根据不同配置段进行基础验证
        if section_name == "webpanel":
            required_fields = ["secret_key"]
            for field in required_fields:
                if field not in config_data:
                    return {
                        "valid": False,
                        "error": f"webpanel配置缺少必需字段: {field}",
                    }

        elif section_name == "queue":
            valid_types = ["memory", "redis", "rabbitmq"]
            queue_type = config_data.get("type")
            if queue_type and queue_type not in valid_types:
                return {
                    "valid": False,
                    "error": f"无效的队列类型: {queue_type}。支持的类型: {valid_types}",
                }

        elif section_name == "logging":
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            log_level = config_data.get("level")
            if log_level and log_level not in valid_levels:
                return {
                    "valid": False,
                    "error": f"无效的日志级别: {log_level}。支持的级别: {valid_levels}",
                }

        return {"valid": True, "error": None}

    except Exception as e:
        return {"valid": False, "error": f"配置验证异常: {str(e)}"}

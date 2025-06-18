"""
认证 API 端点的集成测试
"""

import pytest
import asyncio
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.admin import Admin, AdminLoginLog, LoginStatus
from app.core.security import security_manager


class TestLoginAPI:
    """登录 API 测试"""

    @pytest.mark.asyncio
    async def test_login_success(self, async_client: AsyncClient, test_user: Admin):
        """测试成功登录"""
        response = await async_client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "testpassword123",
                "remember": False
            }
        )

        assert response.status_code == 200
        data = response.json()

        # 验证响应结构
        assert "access_token" in data
        assert "refresh_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
        assert "user" in data

        # 验证用户信息
        user_data = data["user"]
        assert user_data["id"] == test_user.id
        assert user_data["username"] == test_user.username
        assert user_data["full_name"] == test_user.full_name
        assert user_data["is_superadmin"] == test_user.is_superadmin

        # 验证令牌
        payload = security_manager.verify_token(data["access_token"])
        assert payload["sub"] == str(test_user.id)
        assert payload["username"] == test_user.username

    @pytest.mark.asyncio
    async def test_login_invalid_username(self, async_client: AsyncClient):
        """测试无效用户名登录"""
        response = await async_client.post(
            "/api/v1/auth/login",
            json={
                "username": "nonexistentuser",
                "password": "somepassword",
                "remember": False
            }
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "用户名或密码错误"

    @pytest.mark.asyncio
    async def test_login_invalid_password(self, async_client: AsyncClient, test_user: Admin):
        """测试错误密码登录"""
        response = await async_client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "wrongpassword",
                "remember": False
            }
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "用户名或密码错误"

    @pytest.mark.asyncio
    async def test_login_inactive_user(self, async_client: AsyncClient, test_session: AsyncSession):
        """测试禁用用户登录"""
        # 创建一个禁用的用户
        inactive_user = Admin(
            username="inactiveuser",
            hashed_password=security_manager.get_password_hash("password123"),
            full_name="Inactive User",
            is_active=False,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        test_session.add(inactive_user)
        await test_session.commit()

        response = await async_client.post(
            "/api/v1/auth/login",
            json={
                "username": "inactiveuser",
                "password": "password123",
                "remember": False
            }
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "账户已被禁用"

    @pytest.mark.asyncio
    async def test_login_rate_limit(self, async_client: AsyncClient):
        """测试登录速率限制"""
        # 使用唯一的用户名避免与其他测试冲突
        unique_username = f"ratelimituser_{datetime.now().timestamp()}"

        # 进行多次失败登录尝试
        for i in range(6):  # 超过限制（默认是5次）
            response = await async_client.post(
                "/api/v1/auth/login",
                json={
                    "username": unique_username,
                    "password": "wrongpassword",
                    "remember": False
                }
            )

            if i < 5:
                assert response.status_code == 401
            else:
                # 第6次应该被速率限制
                assert response.status_code == 429
                assert "登录尝试次数过多" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_login_creates_log(
        self,
        async_client: AsyncClient,
        test_user: Admin,
        test_db_engine
    ):
        """测试登录创建日志记录"""
        # 执行登录
        response = await async_client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "testpassword123",
                "remember": False
            }
        )

        assert response.status_code == 200

        # 使用新的会话查询日志
        from sqlalchemy.ext.asyncio import AsyncSession
        async with AsyncSession(test_db_engine) as session:
            stmt = select(AdminLoginLog).where(
                AdminLoginLog.admin_id == test_user.id
            )
            result = await session.execute(stmt)
            log = result.scalar_one_or_none()

            assert log is not None
            assert log.status == LoginStatus.SUCCESS
            assert log.failure_reason is None


class TestRefreshTokenAPI:
    """刷新令牌 API 测试"""

    @pytest.mark.asyncio
    async def test_refresh_token_success(self, async_client: AsyncClient, test_user: Admin):
        """测试成功刷新令牌"""
        # 先登录获取刷新令牌
        login_response = await async_client.post(
            "/api/v1/auth/login",
            json={
                "username": "testuser",
                "password": "testpassword123",
                "remember": False
            }
        )

        refresh_token = login_response.json()["refresh_token"]

        # 等待一秒以确保新令牌的时间戳不同
        await asyncio.sleep(1)

        # 使用刷新令牌
        response = await async_client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )

        assert response.status_code == 200
        data = response.json()

        # 验证响应
        assert "access_token" in data
        assert "refresh_token" in data
        # 由于JWT包含时间戳，即使内容相同，新token也应该不同
        assert data["user"]["id"] == test_user.id

    @pytest.mark.asyncio
    async def test_refresh_token_invalid(self, async_client: AsyncClient):
        """测试无效刷新令牌"""
        response = await async_client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid-refresh-token"}
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "无效的认证令牌"

    @pytest.mark.asyncio
    async def test_refresh_token_wrong_type(self, async_client: AsyncClient, test_user: Admin):
        """测试使用访问令牌作为刷新令牌"""
        # 创建一个访问令牌
        token_data = {
            "sub": str(test_user.id),
            "username": test_user.username,
            "is_superadmin": test_user.is_superadmin,
        }
        access_token = security_manager.create_access_token(token_data)

        # 尝试用访问令牌刷新
        response = await async_client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": access_token}
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "无效的刷新令牌"

    @pytest.mark.asyncio
    async def test_refresh_token_expired(self, async_client: AsyncClient, test_user: Admin):
        """测试过期的刷新令牌"""
        # 创建一个过期的刷新令牌
        token_data = {
            "sub": str(test_user.id),
            "username": test_user.username,
            "is_superadmin": test_user.is_superadmin,
            "type": "refresh",
            "exp": datetime.now(timezone.utc) - timedelta(hours=1)  # 已过期
        }

        # 手动创建过期令牌
        expired_token = security_manager.create_refresh_token(token_data)

        # 修改令牌的过期时间（需要直接编码）
        from jose import jwt

        # 解码并修改过期时间
        payload = jwt.decode(
            expired_token,
            security_manager.settings.secret_key,
            algorithms=[security_manager.settings.jwt_algorithm],
            options={"verify_exp": False}
        )
        payload["exp"] = (datetime.now(timezone.utc) -
                          timedelta(hours=1)).timestamp()

        # 重新编码
        expired_token = jwt.encode(
            payload,
            security_manager.settings.secret_key,
            algorithm=security_manager.settings.jwt_algorithm
        )

        response = await async_client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": expired_token}
        )

        assert response.status_code == 401


class TestChangePasswordAPI:
    """修改密码 API 测试"""

    @pytest.mark.asyncio
    async def test_change_password_success(
        self,
        async_client: AsyncClient,
        test_user: Admin,
        auth_headers: dict,
        test_session: AsyncSession,
        test_db_engine
    ):
        """测试成功修改密码"""
        response = await async_client.post(
            "/api/v1/auth/change-password",
            json={
                "old_password": "testpassword123",
                "new_password": "newpassword456",
                "confirm_password": "newpassword456"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        assert response.json()["message"] == "密码修改成功"

        # 从数据库重新查询用户以验证密码已更改
        async with AsyncSession(test_db_engine) as session:
            stmt = select(Admin).where(Admin.id == test_user.id)
            result = await session.execute(stmt)
            updated_user = result.scalar_one()

            assert security_manager.verify_password(
                "newpassword456", updated_user.hashed_password)

    @pytest.mark.asyncio
    async def test_change_password_wrong_old(
        self,
        async_client: AsyncClient,
        auth_headers: dict
    ):
        """测试原密码错误"""
        response = await async_client.post(
            "/api/v1/auth/change-password",
            json={
                "old_password": "wrongoldpassword",
                "new_password": "newpassword456",
                "confirm_password": "newpassword456"
            },
            headers=auth_headers
        )

        assert response.status_code == 400
        assert response.json()["detail"] == "原密码错误"

    @pytest.mark.asyncio
    async def test_change_password_mismatch(
        self,
        async_client: AsyncClient,
        auth_headers: dict
    ):
        """测试新密码不匹配"""
        response = await async_client.post(
            "/api/v1/auth/change-password",
            json={
                "old_password": "testpassword123",
                "new_password": "newpassword456",
                "confirm_password": "differentpassword"
            },
            headers=auth_headers
        )

        # 应该是 422 错误，因为 Pydantic 验证失败
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_change_password_unauthorized(self, async_client: AsyncClient):
        """测试未授权修改密码"""
        response = await async_client.post(
            "/api/v1/auth/change-password",
            json={
                "old_password": "testpassword123",
                "new_password": "newpassword456",
                "confirm_password": "newpassword456"
            }
        )

        assert response.status_code == 403  # 未提供认证头


class TestCurrentUserAPI:
    """当前用户 API 测试"""

    @pytest.mark.asyncio
    async def test_get_current_user(
        self,
        async_client: AsyncClient,
        test_user: Admin,
        auth_headers: dict
    ):
        """测试获取当前用户信息"""
        response = await async_client.get(
            "/api/v1/auth/me",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()

        # API 返回的 id 是字符串
        assert data["id"] == str(test_user.id)
        assert data["username"] == test_user.username
        assert data["is_superadmin"] == test_user.is_superadmin

    @pytest.mark.asyncio
    async def test_get_current_user_unauthorized(self, async_client: AsyncClient):
        """测试未授权获取用户信息"""
        response = await async_client.get("/api/v1/auth/me")

        assert response.status_code == 403


class TestLogoutAPI:
    """登出 API 测试"""

    @pytest.mark.asyncio
    async def test_logout(self, async_client: AsyncClient, auth_headers: dict):
        """测试登出"""
        response = await async_client.post(
            "/api/v1/auth/logout",
            headers=auth_headers
        )

        assert response.status_code == 200
        assert response.json()["message"] == "登出成功"

    @pytest.mark.asyncio
    async def test_logout_unauthorized(self, async_client: AsyncClient):
        """测试未授权登出"""
        response = await async_client.post("/api/v1/auth/logout")

        assert response.status_code == 403

"""
安全模块单元测试
"""

import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.security import security_manager


class TestPasswordHashing:
    """密码哈希测试"""

    def test_password_hashing(self):
        """测试密码哈希功能"""
        password = "test_password_123"
        hashed = security_manager.get_password_hash(password)

        # 验证哈希不等于原密码
        assert hashed != password

        # 验证哈希格式（bcrypt）
        assert hashed.startswith("$2b$")

        # 验证相同密码产生不同哈希（因为盐值）
        hashed2 = security_manager.get_password_hash(password)
        assert hashed != hashed2

    def test_password_verification_success(self):
        """测试密码验证成功"""
        password = "test_password_123"
        hashed = security_manager.get_password_hash(password)

        assert security_manager.verify_password(password, hashed) is True

    def test_password_verification_failure(self):
        """测试密码验证失败"""
        password = "test_password_123"
        wrong_password = "wrong_password"
        hashed = security_manager.get_password_hash(password)

        assert security_manager.verify_password(
            wrong_password, hashed) is False

    def test_password_hash_consistency(self):
        """测试密码哈希一致性"""
        password = "consistent_password"

        # 创建多个哈希
        hashes = [security_manager.get_password_hash(
            password) for _ in range(5)]

        # 验证所有哈希都能正确验证原密码
        for hashed in hashes:
            assert security_manager.verify_password(password, hashed) is True


class TestJWTToken:
    """JWT 令牌测试"""

    def test_create_access_token(self):
        """测试创建访问令牌"""
        data = {
            "sub": "123",
            "username": "testuser",
            "is_superadmin": False
        }

        token = security_manager.create_access_token(data)

        # 验证令牌格式
        assert isinstance(token, str)
        assert len(token.split(".")) == 3  # JWT 格式：header.payload.signature

        # 解码并验证内容
        payload = jwt.decode(
            token,
            security_manager.settings.secret_key,
            algorithms=[security_manager.settings.jwt_algorithm]
        )

        assert payload["sub"] == "123"
        assert payload["username"] == "testuser"
        assert payload["is_superadmin"] is False
        assert "exp" in payload

    def test_create_refresh_token(self):
        """测试创建刷新令牌"""
        data = {
            "sub": "123",
            "username": "testuser",
            "is_superadmin": False
        }

        token = security_manager.create_refresh_token(data)

        # 解码并验证内容
        payload = jwt.decode(
            token,
            security_manager.settings.secret_key,
            algorithms=[security_manager.settings.jwt_algorithm]
        )

        assert payload["sub"] == "123"
        assert payload["username"] == "testuser"
        assert payload["type"] == "refresh"
        assert "exp" in payload

    def test_verify_valid_token(self):
        """测试验证有效令牌"""
        data = {
            "sub": "123",
            "username": "testuser",
            "is_superadmin": True
        }

        token = security_manager.create_access_token(data)
        payload = security_manager.verify_token(token)

        assert payload["sub"] == "123"
        assert payload["username"] == "testuser"
        assert payload["is_superadmin"] is True

    def test_verify_invalid_token(self):
        """测试验证无效令牌"""
        with pytest.raises(Exception) as exc_info:
            security_manager.verify_token("invalid.token.here")

        # 应该抛出 HTTPException
        assert exc_info.value.status_code == 401
        assert "无效的认证令牌" in exc_info.value.detail

    def test_verify_expired_token(self):
        """测试验证过期令牌"""
        # 创建一个立即过期的令牌
        data = {
            "sub": "123",
            "username": "testuser",
            "exp": (datetime.now(timezone.utc) - timedelta(hours=1)).timestamp()
        }

        # 手动创建过期令牌
        expired_token = jwt.encode(
            data,
            security_manager.settings.secret_key,
            algorithm=security_manager.settings.jwt_algorithm
        )

        with pytest.raises(Exception) as exc_info:
            security_manager.verify_token(expired_token)

        assert exc_info.value.status_code == 401

    def test_token_expiration_time(self):
        """测试令牌过期时间设置"""
        data = {"sub": "123", "username": "testuser"}

        # 创建访问令牌
        access_token = security_manager.create_access_token(data)
        access_payload = jwt.decode(
            access_token,
            security_manager.settings.secret_key,
            algorithms=[security_manager.settings.jwt_algorithm]
        )

        # 创建刷新令牌
        refresh_token = security_manager.create_refresh_token(data)
        refresh_payload = jwt.decode(
            refresh_token,
            security_manager.settings.secret_key,
            algorithms=[security_manager.settings.jwt_algorithm]
        )

        # 验证过期时间
        now = datetime.now(timezone.utc).timestamp()

        # 访问令牌应该在配置的小时数后过期
        access_exp_diff = access_payload["exp"] - now
        expected_access_exp = security_manager.settings.jwt_expiration_hours * 3600
        assert abs(access_exp_diff - expected_access_exp) < 10  # 允许10秒误差

        # 刷新令牌应该在7天后过期
        refresh_exp_diff = refresh_payload["exp"] - now
        expected_refresh_exp = 7 * 24 * 3600  # 7天
        assert abs(refresh_exp_diff - expected_refresh_exp) < 10

    def test_token_with_different_algorithms(self):
        """测试使用不同算法的令牌验证失败"""
        data = {"sub": "123", "username": "testuser"}

        # 使用不同的算法创建令牌
        wrong_algo_token = jwt.encode(
            data,
            security_manager.settings.secret_key,
            algorithm="HS512"  # 不同的算法
        )

        # 验证应该失败
        with pytest.raises(Exception):
            security_manager.verify_token(wrong_algo_token)

    def test_token_with_wrong_secret(self):
        """测试使用错误密钥的令牌验证失败"""
        data = {"sub": "123", "username": "testuser"}

        # 使用错误的密钥创建令牌
        wrong_secret_token = jwt.encode(
            data,
            "wrong-secret-key",
            algorithm=security_manager.settings.jwt_algorithm
        )

        # 验证应该失败
        with pytest.raises(Exception):
            security_manager.verify_token(wrong_secret_token)


class TestPasswordStrength:
    """密码强度测试"""

    def test_password_min_length(self):
        """测试密码最小长度要求"""
        from app.core.security import validate_password_strength

        # 测试太短的密码
        assert validate_password_strength("short") is False
        assert validate_password_strength("1234567") is False

        # 测试符合长度要求的密码
        assert validate_password_strength("12345678") is True
        assert validate_password_strength("verylongpassword123") is True

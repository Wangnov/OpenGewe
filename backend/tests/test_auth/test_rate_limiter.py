"""
速率限制器测试
"""

import pytest
import asyncio
from datetime import datetime, timedelta, timezone

from app.core.security import rate_limiter


class TestRateLimiter:
    """速率限制器测试"""

    def test_rate_limiter_initialization(self):
        """测试速率限制器初始化"""
        # 验证速率限制器存在
        assert rate_limiter is not None
        assert hasattr(rate_limiter, 'attempts')
        assert hasattr(rate_limiter, 'is_rate_limited')
        assert hasattr(rate_limiter, 'record_attempt')

    def test_no_rate_limit_initially(self):
        """测试初始状态无速率限制"""
        identifier = "test_user_initial"

        # 初始状态应该没有速率限制
        assert rate_limiter.is_rate_limited(identifier) is False

    def test_rate_limit_after_max_attempts(self):
        """测试达到最大尝试次数后的速率限制"""
        identifier = "test_user_max_attempts"
        max_attempts = rate_limiter.settings.max_login_attempts

        # 清理之前的记录
        rate_limiter.attempts.pop(identifier, None)

        # 记录尝试直到达到限制
        for i in range(max_attempts):
            assert rate_limiter.is_rate_limited(identifier) is False
            rate_limiter.record_attempt(identifier)

        # 达到限制后应该被限制
        assert rate_limiter.is_rate_limited(identifier) is True

    def test_rate_limit_window_expiration(self):
        """测试速率限制窗口过期"""
        identifier = "test_user_window"
        max_attempts = rate_limiter.settings.max_login_attempts

        # 清理之前的记录
        rate_limiter.attempts[identifier] = []

        # 添加过期的尝试记录
        old_time = datetime.now(timezone.utc) - timedelta(minutes=20)
        for _ in range(max_attempts):
            rate_limiter.attempts[identifier].append(old_time)

        # 即使有很多尝试，但都已过期，所以不应该被限制
        assert rate_limiter.is_rate_limited(identifier) is False

    def test_rate_limit_mixed_window(self):
        """测试混合时间窗口的速率限制"""
        identifier = "test_user_mixed"

        # 清理之前的记录
        rate_limiter.attempts[identifier] = []

        # 添加一些过期的尝试
        old_time = datetime.now(timezone.utc) - timedelta(minutes=20)
        for _ in range(3):
            rate_limiter.attempts[identifier].append(old_time)

        # 添加一些新的尝试
        now = datetime.now(timezone.utc)
        for _ in range(3):
            rate_limiter.attempts[identifier].append(now)

        # 只有3个新尝试，不应该被限制
        assert rate_limiter.is_rate_limited(identifier) is False

        # 再添加足够的新尝试达到限制
        for _ in range(2):
            rate_limiter.record_attempt(identifier)

        # 现在应该被限制（5个新尝试）
        assert rate_limiter.is_rate_limited(identifier) is True

    def test_different_identifiers_isolated(self):
        """测试不同标识符之间的隔离"""
        identifier1 = "test_user_1"
        identifier2 = "test_user_2"
        max_attempts = rate_limiter.settings.max_login_attempts

        # 清理之前的记录
        rate_limiter.attempts.pop(identifier1, None)
        rate_limiter.attempts.pop(identifier2, None)

        # 对identifier1记录最大尝试次数
        for _ in range(max_attempts):
            rate_limiter.record_attempt(identifier1)

        # identifier1应该被限制
        assert rate_limiter.is_rate_limited(identifier1) is True

        # identifier2不应该被限制
        assert rate_limiter.is_rate_limited(identifier2) is False

    def test_custom_window_duration(self):
        """测试自定义窗口时长"""
        identifier = "test_user_custom_window"

        # 清理之前的记录
        rate_limiter.attempts[identifier] = []

        # 添加在10分钟窗口内的尝试（比如9分钟前）
        edge_time = datetime.now(timezone.utc) - timedelta(minutes=9)
        for _ in range(5):
            rate_limiter.attempts[identifier].append(edge_time)

        # 使用10分钟窗口，应该被限制
        assert rate_limiter.is_rate_limited(
            identifier, window_minutes=10) is True

        # 使用5分钟窗口，不应该被限制（因为记录在9分钟前）
        assert rate_limiter.is_rate_limited(
            identifier, window_minutes=5) is False

    @pytest.mark.asyncio
    async def test_concurrent_attempts(self):
        """测试并发尝试记录"""
        identifier = "test_user_concurrent"

        # 清理之前的记录
        rate_limiter.attempts.pop(identifier, None)

        # 并发记录尝试
        tasks = []
        for _ in range(10):
            tasks.append(asyncio.create_task(
                asyncio.to_thread(rate_limiter.record_attempt, identifier)
            ))

        await asyncio.gather(*tasks)

        # 验证所有尝试都被记录
        assert len(rate_limiter.attempts[identifier]) == 10

        # 应该被速率限制
        assert rate_limiter.is_rate_limited(identifier) is True

    def test_cleanup_old_attempts(self):
        """测试清理旧尝试记录"""
        identifier = "test_user_cleanup"

        # 添加混合的尝试记录
        rate_limiter.attempts[identifier] = []

        # 旧记录
        old_time = datetime.now(timezone.utc) - timedelta(minutes=30)
        for _ in range(5):
            rate_limiter.attempts[identifier].append(old_time)

        # 新记录
        now = datetime.now(timezone.utc)
        for _ in range(3):
            rate_limiter.attempts[identifier].append(now)

        # 调用is_rate_limited会触发清理
        rate_limiter.is_rate_limited(identifier)

        # 验证旧记录被清理
        assert len(rate_limiter.attempts[identifier]) == 3

    def test_rate_limiter_with_empty_identifier(self):
        """测试空标识符的处理"""
        # 空字符串标识符应该正常工作
        assert rate_limiter.is_rate_limited("") is False

        rate_limiter.record_attempt("")
        assert len(rate_limiter.attempts[""]) == 1

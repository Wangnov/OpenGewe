"""
主配置数据模型
"""

from datetime import datetime, timezone
from sqlalchemy import String, Integer, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column

from ..core.bases import AdminBase
from ..utils.timezone_utils import to_app_timezone


class MainConfig(AdminBase):
    """主配置表"""

    __tablename__ = "main_config"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    section_name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    config_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: to_app_timezone(datetime.now(timezone.utc)),
        onupdate=lambda: to_app_timezone(datetime.now(timezone.utc)),
    )

    def __repr__(self) -> str:
        return f"<MainConfig(id={self.id}, section='{self.section_name}', version={self.version})>"

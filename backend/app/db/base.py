"""数据库基础模型模块

提供SQLAlchemy基础模型类和通用字段定义。
"""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """SQLAlchemy声明式基类

    为所有模型提供id字段和表名推导功能。
    """

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now, index=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # 生成表名: 将类名转换为蛇形命名法
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self) -> Dict[str, Any]:
        """将模型实例转换为字典"""
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Base":
        """从字典创建模型实例"""
        return cls(
            **{
                k: v
                for k, v in data.items()
                if k in [c.name for c in cls.__table__.columns]
            }
        )

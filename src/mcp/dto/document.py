"""
文档查询数据传输对象模块。

提供文档查询参数的封装和 Builder 模式构建器。
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class DocumentQuery:
    """文档查询参数对象。"""

    version: Optional[str] = None
    category: Optional[str] = None
    name: Optional[str] = None

    def __str__(self) -> str:
        return f'DocumentQuery(version={self.version}, category={self.category})'

    @classmethod
    def builder(cls) -> 'DocumentQueryBuilder':
        """创建查询构建器。"""
        return DocumentQueryBuilder(cls)

    @classmethod
    def build(cls, **kwargs) -> 'DocumentQuery':
        """直接构建查询对象。"""
        return cls(**kwargs)


class DocumentQueryBuilder:
    """文档查询构建器，支持链式调用。"""

    def __init__(self, _class: type[DocumentQuery]):
        self._class = _class
        self._data: dict = {}

    def version(self, version: str) -> 'DocumentQueryBuilder':
        """设置版本参数。"""
        self._data['version'] = version
        return self

    def category(self, category: str) -> 'DocumentQueryBuilder':
        """设置分类参数。"""
        self._data['category'] = category
        return self

    def name(self, name: str) -> 'DocumentQueryBuilder':
        """设置名称参数。"""
        self._data['name'] = name
        return self

    def build(self) -> DocumentQuery:
        """
        构建查询对象。

        Raises:
            ValueError: 参数不完整时抛出。
        """
        if not all(self._data.values()):
            raise ValueError("文档查询实体参数错误！")
        return self._class(**self._data)

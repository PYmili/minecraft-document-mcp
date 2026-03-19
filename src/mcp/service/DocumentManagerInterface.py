"""
文档管理服务接口模块。

定义文档查询服务的抽象接口，规范文档管理行为。
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.mcp.dto.document import DocumentQuery
from src.mcp.entity.document import DocumentInformation


class DocumentManagerInterface(ABC):
    """文档管理服务抽象基类。"""

    @staticmethod
    @abstractmethod
    def get_all_document(is_read_context: bool = False) -> List[DocumentInformation]:
        """
        获取所有文档信息。

        Args:
            is_read_context: 是否读取文档详细内容，默认为 False。

        Returns:
            List[DocumentInformation]: 文档信息列表。
        """
        pass

    @staticmethod
    @abstractmethod
    def get_document(query: DocumentQuery) -> Optional[DocumentInformation]:
        """
        根据查询条件获取文档。

        Args:
            query: 文档查询对象，包含 category、version、name 等条件。

        Returns:
            Optional[DocumentInformation]: 匹配的文档信息，未找到时返回 None。
        """
        pass

    @staticmethod
    @abstractmethod
    def get_all_category() -> List[str]:
        """
        获取所有文档分类。

        Returns:
            List[str]: 分类名称列表。
        """
        pass

    @staticmethod
    @abstractmethod
    def get_version(category: str) -> List[str]:
        """
        获取指定分类下的所有版本。

        Args:
            category: 文档分类名称。

        Returns:
            List[str]: 版本名称列表。
        """
        pass
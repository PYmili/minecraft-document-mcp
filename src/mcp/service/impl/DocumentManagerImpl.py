"""
文档管理服务实现模块。

提供文档查询、分类列表、版本列表等核心功能的具体实现。
"""

from typing import List, Optional

from src.mcp.dto.document import DocumentQuery
from src.mcp.entity.document import DocumentInformation
from src.mcp.service.DocumentManagerInterface import DocumentManagerInterface
from src.mcp.utils.DocumentFileUtil import DocumentFileUtil


class DocumentManager(DocumentManagerInterface):
    """文档管理服务实现类。"""

    @staticmethod
    def get_all_document(is_read_context: bool = False) -> List[DocumentInformation]:
        """获取所有文档信息。"""
        category_list = DocumentFileUtil.find_all_category()

        result = []
        for category in category_list:
            info_item = DocumentFileUtil.find_information(category, is_read_context)
            if len(info_item) <= 0:
                continue
            result += info_item

        return result

    @staticmethod
    def get_document(query: DocumentQuery) -> Optional[DocumentInformation]:
        """
        根据查询条件获取文档。

        Raises:
            ValueError: 分类不存在或查询参数错误时抛出。
        """
        category: Optional[str] = query.category
        if category not in DocumentFileUtil.find_all_category():
            raise ValueError(f"分类：{category} 不存在")

        version: Optional[str] = query.version
        name: Optional[str] = query.name
        if not all([category, version, name]):
            raise ValueError(f"{DocumentQuery}的参数错误")

        if not name.endswith(".md"):
            name += ".md"

        infos = DocumentFileUtil.find_information(category, True)

        result = DocumentInformation('', '', '', [])
        for info in infos:
            if version != info.version:
                continue

            for context in info.context:
                if name != context.name:
                    continue
                result.category = info.category
                result.version = info.version
                result.description = info.description
                result.context = [context]

        return result

    @staticmethod
    def get_all_category() -> List[str]:
        """获取所有文档分类。"""
        return DocumentFileUtil.find_all_category()

    @staticmethod
    def get_version(category: str) -> List[str]:
        """获取指定分类下的所有版本。"""
        return DocumentFileUtil.find_version(category)

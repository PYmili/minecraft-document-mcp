"""
Minecraft 文档 MCP 服务器入口模块。

本模块基于 FastMCP 框架实现，为 AI 助手提供 Minecraft 游戏文档的查询服务。
支持通过 MCP 协议获取文档分类、版本信息及详细内容。
"""

from fastmcp import FastMCP

from src.mcp.dto.document import DocumentQuery
from src.mcp.request.WikiApiRequest import WikiApiRequestUtil
from src.mcp.service.impl.DocumentManagerImpl import DocumentManager

mcp = FastMCP("minecraft-document-mcp")


class MinecraftDocumentMcp:
    """Minecraft 文档 MCP 服务工具类。"""

    @staticmethod
    @mcp.tool
    def get_available_info() -> list[dict]:
        """
        获取可用的文档分类和版本信息。

        Returns:
            list[dict]: 可用的分类信息列表，每项包含:
                - 分类 (str): 文档分类名称
                - 版本列表 (list[str]): 该分类下的版本列表
        """
        result = []
        category_list = DocumentManager.get_all_category()
        for category in category_list:
            version = DocumentManager.get_version(category)
            result.append({"分类": category, "版本列表": version})
        return result

    @staticmethod
    @mcp.tool
    def get_all_partial_info() -> list[dict]:
        """
        获取所有文档的部分信息（不含详细内容）。

        Returns:
            list[dict]: 文档信息列表，每项包含:
                - version: 版本
                - category: 分类
                - description: 描述
                - context: 文档内容列表 (context 字段为空)
        """
        return [doc.to_dict()
                for doc in DocumentManager.get_all_document()]

    @staticmethod
    @mcp.tool
    def get_document_context(category: str, version: str, name: str) -> list[dict]:
        """
        根据参数获取详细的文档内容。

        Args:
            category: 文档分类，如 "command"。
            version: 文档版本，如 "java"。
            name: 文档名称，如 "list.md"。

        Returns:
            list[dict]: 文档内容列表，包含 name、description、context 字段。
        """
        query = (DocumentQuery.builder()
                 .category(category)
                 .version(version)
                 .name(name)
                 .build())
        document = DocumentManager.get_document(query)
        if document is None:
            return []

        context = (document.to_dict().get("context"))
        return context

    @staticmethod
    @mcp.tool
    def search_wiki_intro(keyword: str) -> str:
        """
        从 Minecraft Wiki 搜索词条简介。

        Args:
            keyword: 搜索关键词，如 "村民"、"钻石"。

        Returns:
            str: Markdown 格式的词条简介。
        """
        return WikiApiRequestUtil.search_exintro(keyword)

    @staticmethod
    @mcp.tool
    def search_wiki_full(keyword: str) -> str:
        """
        从 Minecraft Wiki 搜索词条完整内容。

        Args:
            keyword: 搜索关键词。

        Returns:
            str: Markdown 格式的完整词条内容。
        """
        return WikiApiRequestUtil.search(keyword)


if __name__ == "__main__":
    mcp.run(transport="sse")
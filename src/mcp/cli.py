"""
MCP 服务器命令行入口模块。
"""

from fastmcp import FastMCP

from src.mcp.api.WikiApi import WikiApiRequestUtil

mcp = FastMCP("minecraft-document-mcp")


class MinecraftDocumentMcp:
    """Minecraft 文档 MCP 服务工具类。"""

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
        return WikiApiRequestUtil.search_intro(keyword)

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

    @staticmethod
    @mcp.tool
    def get_wiki_categories() -> list[dict]:
        """
        获取 Wiki 首页的主要分类列表。

        Returns:
            list[dict]: 分类列表，每项包含 name 和 description 字段。
        """
        return WikiApiRequestUtil.get_category()


def main():
    """MCP 服务器入口函数。"""
    mcp.run()
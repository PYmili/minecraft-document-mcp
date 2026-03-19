"""
Minecraft 文档 MCP 服务器入口模块。

本模块基于 FastMCP 框架实现，为 AI 助手提供 Minecraft Wiki 文档查询服务。
支持通过 MCP 协议从中文 Minecraft Wiki 获取词条内容。
"""

from fastmcp import FastMCP

from src.mcp.request.WikiApiRequest import WikiApiRequestUtil

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
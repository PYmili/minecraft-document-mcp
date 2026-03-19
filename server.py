"""
Minecraft 文档 MCP 服务器入口模块。

本模块基于 FastMCP 框架实现，为 AI 助手提供 Minecraft Wiki 文档查询服务。
支持通过 MCP 协议从中文 Minecraft Wiki 获取词条内容。
"""

from src.mcp.cli import mcp, main

if __name__ == "__main__":
    main()
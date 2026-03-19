# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 Minecraft 文档 MCP (Model Context Protocol) 服务器，使用 FastMCP 框架构建，从中文 Minecraft Wiki 获取游戏文档内容。

## 常用命令

```bash
# 启动 MCP 服务器 (SSE 传输模式)
python server.py

# 或者使用 fastmcp dev 开发模式
fastmcp dev server.py
```

## 架构

### 项目结构

```
server.py                       # 入口文件，定义 MCP 工具端点
src/mcp/request/
└── WikiApiRequest.py           # Wiki API 请求工具
```

### MCP 工具

server.py 中定义了两个 MCP 工具：

- `search_wiki_intro`: 搜索词条简介
- `search_wiki_full`: 搜索词条完整内容

### WikiApiRequest 功能

- `search_exintro(text)`: 获取词条简介（Markdown 格式）
- `search(text)`: 获取完整词条内容（Markdown 格式）
- 使用 BeautifulSoup 解析 HTML，markdownify 转换为 Markdown

## 依赖

- Python 3.12+
- fastmcp==3.1.1
- beautifulsoup4
- lxml
- markdownify
- requests
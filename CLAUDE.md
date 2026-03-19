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
src/mcp/api/
├── WikiApi.py                  # Wiki API 请求工具
└── WikiItems.py                # 数据项定义 (CategoryItem)
```

### 核心类

| 类名 | 职责 |
|-----|------|
| `WikiApiClient` | HTTP 请求客户端，负责发送请求和处理响应 |
| `ContentCleaner` | HTML 内容清理工具，移除冗余元素 |
| `WikiApiRequestUtil` | 文档查询工具类，对外暴露的主要接口 |

### MCP 工具

- `search_wiki_intro`: 搜索词条简介
- `search_wiki_full`: 搜索词条完整内容
- `get_wiki_categories`: 获取 Wiki 首页主要分类列表

## 依赖

- Python 3.12+
- fastmcp==3.1.1
- beautifulsoup4
- lxml
- markdownify
- requests
- dataclasses-json
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 Minecraft 文档 MCP (Model Context Protocol) 服务器，使用 FastMCP 框架构建，为 AI 助手提供 Minecraft 游戏文档查询功能。

## 常用命令

```bash
# 启动 MCP 服务器 (SSE 传输模式)
python server.py

# 或者使用 fastmcp dev 开发模式
fastmcp dev server.py
```

## 架构

### 分层结构

```
server.py                 # 入口文件，定义 MCP 工具端点
src/mcp/
├── service/              # 服务层
│   ├── DocumentManagerInterface.py    # 抽象接口
│   └── impl/DocumentManagerImpl.py    # 实现
├── dto/document.py       # 数据传输对象 (DocumentQuery + Builder)
├── entity/document.py    # 实体类 (DocumentInformation, DocumentContext)
└── utils/DocumentFileUtil.py  # 文件操作工具
src/resources/document/   # 文档存储目录
```

### 文档存储结构

```
src/resources/document/
└── {category}/           # 分类 (如: command)
    └── {version}/        # 版本 (如: java)
        ├── .json         # 元数据 (version, category, description, context 列表)
        └── *.md          # 实际文档文件
```

### MCP 工具

server.py 中定义了三个 MCP 工具：

- `get_available_info`: 获取所有分类和版本信息
- `get_all_partial_info`: 获取文档摘要列表（不含详细内容）
- `get_document_context`: 根据分类、版本、名称获取完整文档内容

### 设计模式

- Builder 模式: `DocumentQuery` 使用 Builder 构建查询对象
- 接口抽象: `DocumentManagerInterface` 定义服务契约
- 缓存: `DocumentFileUtil` 使用模块级 `CACHE` 字典缓存查询结果

## 依赖

- Python 3.12+
- fastmcp==3.1.1
- dataclasses-json>=0.6.7
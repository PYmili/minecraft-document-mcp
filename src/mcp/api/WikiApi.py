"""
Minecraft Wiki API 请求工具模块。

基于 MediaWiki API 从中文 Minecraft Wiki 获取游戏相关文档内容，
支持获取词条简介和完整内容（转换为 Markdown 格式）。
"""

import json
from typing import Optional, List

import requests
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify

from src.mcp.api.WikiItems import CategoryItem

API_HOST = "https://zh.minecraft.wiki/"

# MediaWiki API 基础配置（获取 HTML 格式内容）
API_URL = (
    API_HOST +
    "api.php"
    "?action=query"
    "&format=json"
    "&prop=extracts|info"
    "&redirects=true"
    "&inprop=url"
    "&variant=zh-cn"
)


def remove_empty_tags(element: Tag) -> None:
    """
    递归移除空的 HTML 标签。

    Args:
        element: BeautifulSoup Tag 对象，将递归处理其子元素。
    """
    for child in list(element.children):
        if not isinstance(child, Tag):
            continue
        remove_empty_tags(child)
        if len(child.text.strip()) == 0:
            child.decompose()


def extract_sprite_title(element: Tag) -> None:
    """
    将精灵图片标签替换为其链接标题文本。

    处理 Wiki 中的 sprite-file span，提取内部 a 标签的 title 属性，
    用于在 Markdown 中保留图片对应的文本描述。

    Args:
        element: BeautifulSoup Tag 对象。
    """
    sprite_files = element.find_all('span', class_='sprite-file')
    for sprite in sprite_files:
        link = sprite.find('a')
        if link is None:
            continue

        title = link.attrs.get('title')
        img = link.find('img')

        # 仅处理有标题或包含图片的链接
        if title is None and img is None:
            continue

        sprite.clear()
        sprite.string = f'{title} '


class WikiApiRequestUtil:
    """Minecraft Wiki API 请求工具类。"""

    request: Optional[requests.Response] = None

    @staticmethod
    def get_request_instance(url: str = API_URL, method: str = 'GET') -> Optional[requests.Response]:
        """
        获取或创建 HTTP 请求实例（单例模式）。

        Args:
            url: 请求地址，默认为 API_HOST。
            method: HTTP 方法，默认为 GET。

        Returns:
            Optional[requests.Response]: HTTP 响应对象。
        """
        if WikiApiRequestUtil.request is None:
            WikiApiRequestUtil.request = requests.request(url=url, method=method)
        return WikiApiRequestUtil.request

    @staticmethod
    def _get_json(url: str) -> Optional[dict]:
        """
        发送请求并解析 JSON 响应。

        Args:
            url: 完整的 API 请求地址。

        Returns:
            Optional[dict]: 解析后的页面数据，页面不存在时返回 None。

        Raises:
            RuntimeError: JSON 解析失败时抛出。
        """
        with WikiApiRequestUtil.get_request_instance(url) as response:
            if not response.ok:
                return None

            try:
                data: dict = response.json()
                pages = data.get("query").get("pages")
                # 页面不存在时，API 返回 {"-1": {...}}
                if len(pages.keys()) == 1 and list(pages.keys())[0] == '-1':
                    return None
                return pages
            except json.JSONDecodeError:
                raise RuntimeError(f'获取 {url} 的数据失败')

    @staticmethod
    def search_exintro(text: str) -> str:
        """
        搜索词条并获取简介内容（Markdown 格式）。

        Args:
            text: 搜索关键词，如 "村民"、"钻石"。

        Returns:
            str: Markdown 格式的词条简介，未找到时返回提示信息。
        """
        url = API_URL + f'&exintro=true&titles={text}'
        pages = WikiApiRequestUtil._get_json(url)

        if pages is None:
            return f'暂无 **{text}** 的简介'

        page_data = pages.get(list(pages.keys())[0])
        extract = page_data.get('extract', '')

        if not extract:
            return f'暂无 **{text}** 的简介'

        # 将 HTML 转换为 Markdown
        return markdownify(extract).strip()

    @staticmethod
    def search(text: str) -> str:
        """
        搜索词条并获取完整内容（Markdown 格式）。

        Args:
            text: 搜索关键词。

        Returns:
            str: 转换为 Markdown 格式的词条内容，获取失败时返回提示信息。
        """
        url = API_URL + f'&exintro=true&titles={text}'
        pages = WikiApiRequestUtil._get_json(url)

        if pages is None:
            return f'暂无 **{text}** 的内容'

        full_url = pages.get(list(pages.keys())[0]).get('fullurl')
        with requests.get(full_url) as response:
            if not response.ok:
                return f'获取 **{text}** 失败'

            soup = BeautifulSoup(response.text, 'lxml')
            content = soup.find('div', id='mw-content-text', class_='mw-body-content')

            if content is None:
                return f'获取 **{text}** 的内容失败'

            # ===== 内容清理 =====
            # 提取精灵图片的标题文本
            extract_sprite_title(content)

            # 移除图片标签
            for img in list(content.find_all('img')):
                img.decompose()

            # 移除编辑链接 '[编辑 | 编辑源代码]'
            for edit_section in content.find_all('span', class_='mw-editsection'):
                edit_section.decompose()

            # 移除目录
            for toc in content.find_all('div', id='toc', class_='toc'):
                toc.decompose()

            # 移除底部导航信息表
            navboxes = content.find_all(
                'table',
                class_='navbox hlist collapsible navigation-not-searchable noresize'
            )
            for navbox in navboxes:
                navbox.decompose()

            # 移除打印页脚
            for footer in content.find_all('div', class_='printfooter'):
                footer.decompose()

            # 解包 a 标签，保留内部文本
            for link in soup.find_all('a'):
                link.unwrap()

            # 移除无内容的空标签（可选）
            # remove_empty_tags(content)

            return markdownify(str(content))

    @staticmethod
    def get_category() -> List[dict]:
        """
        获取 Wiki 首页的主要分类列表。

        从中文 Minecraft Wiki 首页抓取主要分类图标，
        返回分类名称及其简介。

        Returns:
            List[dict]: 分类列表，每项包含:
                - name: 分类名称
                - description: 分类简介
        """
        result = []
        with requests.get(API_HOST) as response:
            if not response.ok:
                return result

            soup = BeautifulSoup(response.text, 'lxml')
            # 定位首页主图标区域
            main_icons = soup.find('div', class_='mp-icon-wrapper mp-main-icons')
            if main_icons is None:
                return result

            # 遍历所有分类图标
            for icon in main_icons.find_all('div', class_='mp-icon'):
                link = icon.find('a')
                if link is None:
                    continue

                title = link.attrs.get('title')
                if title is None:
                    continue

                # 获取该分类的简介
                intro = WikiApiRequestUtil.search_exintro(title)
                result.append(CategoryItem(title, intro).to_dict())

        return result

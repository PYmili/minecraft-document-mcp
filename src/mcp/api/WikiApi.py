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

# Wiki 基础地址
API_HOST = "https://zh.minecraft.wiki/"

# MediaWiki API 基础配置
API_URL = (
    f"{API_HOST}api.php"
    "?action=query"
    "&format=json"
    "&prop=extracts|info"
    "&redirects=true"
    "&inprop=url"
    "&variant=zh-cn"
)


class ContentCleaner:
    """HTML 内容清理工具类。"""

    @staticmethod
    def remove_empty_tags(element: Tag) -> None:
        """
        递归移除空的 HTML 标签。

        Args:
            element: BeautifulSoup Tag 对象。
        """
        for child in list(element.children):
            if not isinstance(child, Tag):
                continue
            ContentCleaner.remove_empty_tags(child)
            if not child.text.strip():
                child.decompose()

    @staticmethod
    def extract_sprite_title(element: Tag) -> None:
        """
        将精灵图片标签替换为其链接标题文本。

        Args:
            element: BeautifulSoup Tag 对象。
        """
        for sprite in element.find_all('span', class_='sprite-file'):
            link = sprite.find('a')
            if link is None:
                continue

            title = link.attrs.get('title')
            img = link.find('img')

            if title is None and img is None:
                continue

            sprite.clear()
            sprite.string = f'{title} ' if title else ''

    @staticmethod
    def clean(content: Tag) -> None:
        """
        清理 Wiki 页面内容，移除冗余元素。

        Args:
            content: BeautifulSoup Tag 对象，通常为 mw-content-text div。
        """
        # 提取精灵图片的标题文本
        ContentCleaner.extract_sprite_title(content)

        # 移除图片标签
        for img in list(content.find_all('img')):
            img.decompose()

        # 移除编辑链接
        for edit_section in content.find_all('span', class_='mw-editsection'):
            edit_section.decompose()

        # 移除目录
        for toc in content.find_all('div', id='toc', class_='toc'):
            toc.decompose()

        # 移除底部导航信息表
        navbox_class = 'navbox hlist collapsible navigation-not-searchable noresize'
        for navbox in content.find_all('table', class_=navbox_class):
            navbox.decompose()

        # 移除打印页脚
        for footer in content.find_all('div', class_='printfooter'):
            footer.decompose()

        # 解包 a 标签，保留内部文本
        for link in content.find_all('a'):
            link.unwrap()


class WikiApiClient:
    """Wiki API 客户端，负责 HTTP 请求和响应处理。"""

    @staticmethod
    def fetch_json(url: str) -> Optional[dict]:
        """
        发送 GET 请求并返回 JSON 数据。

        Args:
            url: 完整的 API 请求地址。

        Returns:
            Optional[dict]: 解析后的页面数据，页面不存在或请求失败时返回 None。

        Raises:
            RuntimeError: JSON 解析失败时抛出。
        """
        response = requests.get(url, timeout=30)
        if not response.ok:
            return None

        try:
            data: dict = response.json()
            pages = data.get("query", {}).get("pages", {})

            # 页面不存在时，API 返回 {"-1": {...}}
            if len(pages) == 1 and list(pages.keys())[0] == '-1':
                return None

            return pages
        except json.JSONDecodeError:
            raise RuntimeError(f'获取 {url} 的数据失败')

    @staticmethod
    def fetch_html(url: str) -> Optional[str]:
        """
        发送 GET 请求并返回 HTML 内容。

        Args:
            url: 完整的页面地址。

        Returns:
            Optional[str]: HTML 内容，请求失败时返回 None。
        """
        response = requests.get(url, timeout=30)
        return response.text if response.ok else None


class WikiApiRequestUtil:
    """Minecraft Wiki 文档查询工具类。"""

    @staticmethod
    def search_intro(text: str) -> str:
        """
        搜索词条并获取简介内容（Markdown 格式）。

        Args:
            text: 搜索关键词，如 "村民"、"钻石"。

        Returns:
            str: Markdown 格式的词条简介，未找到时返回提示信息。
        """
        url = f"{API_URL}&exintro=true&titles={text}"
        pages = WikiApiClient.fetch_json(url)

        if pages is None:
            return f'暂无 **{text}** 的简介'

        page_data = pages.get(list(pages.keys())[0], {})
        extract = page_data.get('extract', '')

        if not extract:
            return f'暂无 **{text}** 的简介'

        return markdownify(extract).strip()

    @staticmethod
    def search(text: str) -> str:
        """
        搜索词条并获取完整内容（Markdown 格式）。

        Args:
            text: 搜索关键词。

        Returns:
            str: Markdown 格式的词条内容，获取失败时返回提示信息。
        """
        url = f"{API_URL}&exintro=true&titles={text}"
        pages = WikiApiClient.fetch_json(url)

        if pages is None:
            return f'暂无 **{text}** 的内容'

        full_url = pages.get(list(pages.keys())[0], {}).get('fullurl')
        if not full_url:
            return f'获取 **{text}** 的链接失败'

        html = WikiApiClient.fetch_html(full_url)
        if html is None:
            return f'获取 **{text}** 失败'

        soup = BeautifulSoup(html, 'lxml')
        content = soup.find('div', id='mw-content-text', class_='mw-body-content')

        if content is None:
            return f'获取 **{text}** 的内容失败'

        # 清理内容
        ContentCleaner.clean(content)

        return markdownify(str(content))

    @staticmethod
    def get_category() -> List[dict]:
        """
        获取 Wiki 首页的主要分类列表。

        Returns:
            List[dict]: 分类列表，每项包含 name 和 description 字段。
        """
        html = WikiApiClient.fetch_html(API_HOST)
        if html is None:
            return []

        soup = BeautifulSoup(html, 'lxml')
        main_icons = soup.find('div', class_='mp-icon-wrapper mp-main-icons')

        if main_icons is None:
            return []

        result = []
        for icon in main_icons.find_all('div', class_='mp-icon'):
            link = icon.find('a')
            if link is None:
                continue

            title = link.attrs.get('title')
            if title is None:
                continue

            intro = WikiApiRequestUtil.search_intro(title)
            result.append(CategoryItem(title, intro).to_dict())

        return result


if __name__ == '__main__':
    print(WikiApiRequestUtil.get_category())
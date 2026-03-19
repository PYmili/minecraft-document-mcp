"""
文档文件工具模块。

提供文档文件的读取、查询和缓存功能。
"""

import json
from pathlib import Path
from typing import List

from src.mcp.entity.document import DocumentInformation, DocumentInformationUtil

CACHE = {}
PROJECT_ROOT = next(
    p for p in Path(__file__).resolve().parents
    if any((p / m).exists() for m in ["pyproject.toml", "server.py"])
)
DOCUMENT_PATH = PROJECT_ROOT / "src" / "resources" / "document"


class DocumentFileUtil:
    """文档文件操作工具类。"""

    @staticmethod
    def _file_ex(path: Path) -> Path:
        """
        检查文件路径是否存在。

        Args:
            path: 待检查的路径。

        Returns:
            Path: 存在的路径。

        Raises:
            FileNotFoundError: 路径不存在时抛出。
        """
        if not path.exists():
            raise FileNotFoundError(f"{path} 不存在！")
        return path

    @staticmethod
    def find_all_category() -> List[str]:
        """
        获取所有文档分类目录名。

        Returns:
            List[str]: 分类名称列表。
        """
        if CACHE.get('category_list'):
            return CACHE.get('category_list')
        path = DocumentFileUtil._file_ex(DOCUMENT_PATH)
        return [_dir.name for _dir in list(path.iterdir()) if _dir.is_dir()]

    @staticmethod
    def find_version(category: str) -> List[str]:
        """
        获取指定分类下的所有版本目录名。

        Args:
            category: 文档分类名称。

        Returns:
            List[str]: 版本名称列表。

        Raises:
            ValueError: 分类不存在时抛出。
        """
        cache_key = f"{category}_version"
        if CACHE.get(cache_key):
            return CACHE.get(cache_key)

        if category not in DocumentFileUtil.find_all_category():
            raise ValueError(f"分类 {category} 不存在")
        path = DocumentFileUtil._file_ex(DOCUMENT_PATH / category)
        return [str(v.name) for v in list(path.iterdir()) if v.is_dir()]

    @staticmethod
    def find_information(category: str, is_read_context: bool = False) -> List[DocumentInformation]:
        """
        获取指定分类下的文档信息。

        Args:
            category: 文档分类名称。
            is_read_context: 是否读取文档详细内容，默认为 False。

        Returns:
            List[DocumentInformation]: 文档信息列表。
        """
        path = DocumentFileUtil._file_ex(DOCUMENT_PATH / category)

        if CACHE.get(str(path)) and not is_read_context:
            return CACHE.get(str(path))

        files: List[Path] = [f for f in list(path.rglob('*'))
                             if f.is_file() and f.name == ".json"]

        result = []
        for file in files:
            info: dict = json.loads(file.read_text("utf-8"))

            if not is_read_context:
                result.append(info)
                continue

            for context in info.get('context', []):
                doc_context = DocumentFileUtil.get_file_context(
                    info.get("category"), info.get("version"), context.get("name")
                )
                context['context'] = doc_context

            result.append(info)

        return DocumentInformationUtil.format(result)

    @staticmethod
    def get_file_context(category: str, version: str, filename: str) -> str:
        """
        读取文档文件内容。

        Args:
            category: 文档分类名称。
            version: 文档版本。
            filename: 文档文件名。

        Returns:
            str: 文档文件内容。
        """
        md_file = DocumentFileUtil._file_ex(DOCUMENT_PATH / category / version / filename)
        with open(md_file, "r", encoding="utf-8") as f:
            return f.read()

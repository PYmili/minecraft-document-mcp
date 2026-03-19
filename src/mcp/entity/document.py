"""
文档实体类模块。

定义文档内容和文档信息的结构化数据对象。
"""

from dataclasses import dataclass
from typing import List

from dataclasses_json import DataClassJsonMixin


@dataclass
class DocumentContext(DataClassJsonMixin):
    """文档内容对象，包含单个文档的基本信息和正文。"""

    name: str
    description: str
    context: str


@dataclass
class DocumentInformation(DataClassJsonMixin):
    """文档信息对象，包含版本、分类及文档内容列表。"""

    version: str
    category: str
    description: str
    context: List[DocumentContext]


class DocumentContextUtil:
    """文档内容工具类，用于字典到对象的转换。"""

    @staticmethod
    def format(args: List[dict]) -> List[DocumentContext]:
        """
        将字典列表转换为 DocumentContext 对象列表。

        Args:
            args: 包含 name、description、context 字段的字典列表。

        Returns:
            List[DocumentContext]: 转换后的对象列表。
        """
        result = []
        for item in args:
            result.append(DocumentContext(
                item["name"],
                item["description"],
                item.get("context", '')
            ))
        return result


class DocumentInformationUtil:
    """文档信息工具类，用于字典到对象的转换。"""

    @staticmethod
    def format(args: List[dict]) -> List[DocumentInformation]:
        """
        将字典列表转换为 DocumentInformation 对象列表。

        Args:
            args: 包含 version、category、description、context 字段的字典列表。

        Returns:
            List[DocumentInformation]: 转换后的对象列表。
        """
        result = []
        for item in args:
            result.append(DocumentInformation(
                item["version"],
                item["category"],
                item["description"],
                DocumentContextUtil.format(item["context"])
            ))
        return result

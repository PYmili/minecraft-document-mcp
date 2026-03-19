"""
Wiki API 数据项定义模块。

定义用于 Wiki API 响应的数据结构。
"""

from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin


@dataclass
class CategoryItem(DataClassJsonMixin):
    """
    分类条目数据类。

    用于表示从 Wiki 首页获取的分类信息。

    Attributes:
        name: 分类名称。
        description: 分类描述（词条简介）。
    """

    name: str
    description: str
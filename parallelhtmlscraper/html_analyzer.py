"""Base classes of HTML analyzer."""
from abc import ABC
from typing import Generic, TypeVar

from bs4 import BeautifulSoup  # type: ignore

__all__ = ["HtmlAnalyzer"]

# noinspection PyShadowingBuiltins
_T = TypeVar("_T")


class HtmlAnalyzer(Generic[_T], ABC):
    async def execute(self, soup: BeautifulSoup) -> _T:
        raise NotImplementedError()

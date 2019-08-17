from abc import ABC
from typing import TypeVar, Generic

from bs4 import BeautifulSoup
__all__ = ['HtmlAnalyzer']

# noinspection PyShadowingBuiltins
_T = TypeVar('_T')


class HtmlAnalyzer(Generic[_T], ABC):
    async def execute(self, soup: BeautifulSoup) -> _T:
        raise NotImplementedError()

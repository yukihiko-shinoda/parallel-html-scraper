# Copyright (C) 2019 Yukihiko Shinoda
"""Base classes of HTML analyzer."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar

if TYPE_CHECKING:
    from bs4 import BeautifulSoup

__all__ = ["HtmlAnalyzer"]

# noinspection PyShadowingBuiltins
_T = TypeVar("_T")


class HtmlAnalyzer(ABC, Generic[_T]):
    async def execute(self, soup: BeautifulSoup) -> _T:
        raise NotImplementedError

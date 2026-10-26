# Copyright (C) 2019 Yukihiko Shinoda
"""Analizer for test."""

from __future__ import annotations

from typing import TYPE_CHECKING

from parallelhtmlscraper.html_analyzer import HtmlAnalyzer

if TYPE_CHECKING:
    from bs4 import BeautifulSoup


class AnalyzerForTest(HtmlAnalyzer[str]):
    async def execute(self, soup: BeautifulSoup) -> str:
        title = soup.title
        assert title is not None
        return title.text

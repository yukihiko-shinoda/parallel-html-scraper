"""Analizer for test."""
from bs4 import BeautifulSoup  # type: ignore

from parallelhtmlscraper.html_analyzer import HtmlAnalyzer


class AnalyzerForTest(HtmlAnalyzer):
    async def execute(self, soup: BeautifulSoup) -> str:
        return soup.find("title").text

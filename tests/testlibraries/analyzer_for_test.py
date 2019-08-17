from bs4 import BeautifulSoup

from parallelhtmlscraper.html_analyzer import HtmlAnalyzer


class AnalyzerForTest(HtmlAnalyzer):
    async def execute(self, soup: BeautifulSoup) -> str:
        return soup.find('title').text

import pytest
from bs4 import BeautifulSoup

from parallelhtmlscraper import HtmlAnalyzer
from tests.testlibraries.instance_resource import InstanceResource


class TestHtmlAnalyzer:
    @staticmethod
    @pytest.mark.asyncio
    async def test():
        class SampleHtmlAnalyzer(HtmlAnalyzer):
            async def execute(self, soup):
                return await super().execute(soup)
        with pytest.raises(NotImplementedError):
            await SampleHtmlAnalyzer().execute(
                BeautifulSoup(InstanceResource.PATH_FILE_HTML_GOOGLE_SEARCH.read_bytes(), 'html.parser')
            )

"""Test for html_analyzer."""
import pytest
from bs4 import BeautifulSoup  # type: ignore

from parallelhtmlscraper import HtmlAnalyzer


class TestHtmlAnalyzer:
    """Test for HtmlAnalyzer."""

    @staticmethod
    @pytest.mark.asyncio
    async def test(resource_path_root):
        """Tests."""

        class SampleHtmlAnalyzer(HtmlAnalyzer):
            async def execute(self, soup):
                return await super().execute(soup)

        with pytest.raises(NotImplementedError):
            await SampleHtmlAnalyzer().execute(
                BeautifulSoup((resource_path_root / "google_search.html").read_bytes(), "html.parser")
            )

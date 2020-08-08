"""Test for html_text_load_coroutine."""
import pytest
from aiohttp import ClientResponse

from parallelhtmlscraper.html_text_load_coroutine import HtmlTextLoadCoroutine
from tests.conftest import AioresponseParameterHtmlByte


class TestHtmlTextRoadCoroutine:
    """Test for HtmlTextRoadCoroutine."""

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "client_response_html_byte",
        [AioresponseParameterHtmlByte("emoji.html", {"charset": "", "Content-Type": "text/html"})],
        indirect=["client_response_html_byte"],
    )
    async def test(client_response_html_byte: ClientResponse):
        """Tests."""
        soup = await HtmlTextLoadCoroutine.execute(client_response_html_byte)
        body = soup.find("body")
        assert body.text.strip() == "あ💫"

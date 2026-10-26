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

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "client_response_from_local_server",
        [AioresponseParameterHtmlByte("emoji.html", {"Content-Type": "text/html; charset=ascii"})],
        indirect=["client_response_from_local_server"],
    )
    async def test_execute_fallback_to_utf_8(client_response_from_local_server: ClientResponse) -> None:
        """Body which can't be decoded by the charset in the header should be decoded as UTF-8."""
        soup = await HtmlTextLoadCoroutine.execute(client_response_from_local_server)
        assert soup.find("body").text.strip() == "あ💫"

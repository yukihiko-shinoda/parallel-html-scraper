# Copyright (C) 2019 Yukihiko Shinoda
"""Test for html_text_load_coroutine."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from parallelhtmlscraper.html_text_load_coroutine import HtmlTextLoadCoroutine
from tests.conftest import AioresponseParameterHtmlByte

if TYPE_CHECKING:
    from aiohttp import ClientResponse


class TestHtmlTextRoadCoroutine:
    """Test for HtmlTextRoadCoroutine."""

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "client_response_html_byte",
        [AioresponseParameterHtmlByte("emoji.html", {"charset": "", "Content-Type": "text/html"})],
        indirect=["client_response_html_byte"],
    )
    async def test(client_response_html_byte: ClientResponse) -> None:
        """Tests."""
        soup = await HtmlTextLoadCoroutine.execute(client_response_html_byte)
        assert soup.body is not None
        assert soup.body.text.strip() == "あ💫"

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
        assert soup.body is not None
        assert soup.body.text.strip() == "あ💫"

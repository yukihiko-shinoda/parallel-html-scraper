# Copyright (C) 2019 Yukihiko Shinoda
"""Test for test_html_request_coroutine."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import aiohttp
import pytest

from parallelhtmlscraper import HttpTimeoutError
from parallelhtmlscraper.html_request_coroutine import HtmlRequestCoroutine
from tests.testlibraries.analyzer_for_test import AnalyzerForTest

if TYPE_CHECKING:
    from pathlib import Path

    from aioresponses import aioresponses


async def mock_sleep(_delay: float) -> None:
    """Skip waiting to speed up the test."""


class TestHtmlRequestCoroutine:
    """Test for HtmlRequestCoroutine."""

    @staticmethod
    @pytest.mark.asyncio
    async def test(
        monkeypatch: pytest.MonkeyPatch,
        mock_aioresponse: aioresponses,
        resource_path_root: Path,
    ) -> None:
        """Tests."""
        monkeypatch.setattr(asyncio, "sleep", mock_sleep)
        url_google = "http://www.google.co.jp/webhp?tab=rw"
        mock_aioresponse.get(url_google, status=200, body=(resource_path_root / "google_search.html").read_bytes())
        async with aiohttp.ClientSession() as session:
            analyze_result = await HtmlRequestCoroutine().execute(session, url_google, AnalyzerForTest())
            assert analyze_result == "Google"

    @staticmethod
    @pytest.mark.asyncio
    async def test_timeout_error(mock_aioresponse: aioresponses) -> None:
        """Tests timeout error."""
        url_google = "http://www.google.co.jp/webhp?tab=rw"
        mock_aioresponse.get(url_google, status=200, exception=asyncio.TimeoutError())
        async with aiohttp.ClientSession() as session:
            with pytest.raises(HttpTimeoutError) as error:
                await HtmlRequestCoroutine().execute(session, url_google, AnalyzerForTest())
        assert str(error.value) == f"HttpTimeoutError. URL = {url_google}"

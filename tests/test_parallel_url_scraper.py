# Copyright (C) 2019 Yukihiko Shinoda
"""Tests for parallel_url_scraper."""

from __future__ import annotations

import asyncio
import os
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

from parallelhtmlscraper.html_request_coroutine import HtmlRequestCoroutine
from parallelhtmlscraper.html_text_load_coroutine import HtmlTextLoadCoroutine
from parallelhtmlscraper.parallel_html_scraper import ParallelHtmlScraper
from tests.testlibraries.analyzer_for_test import AnalyzerForTest

if TYPE_CHECKING:
    from pathlib import Path

    import pytest
    from aiohttp import ClientResponse
    from aioresponses import aioresponses
    from pytest_mock import MockerFixture


class HtmlTextLoadCoroutineForSimulateProcessTime(HtmlTextLoadCoroutine):
    @classmethod
    async def execute(cls, response: ClientResponse) -> BeautifulSoup:
        await asyncio.sleep(5.1)
        return BeautifulSoup(await super()._execute(response), "html.parser")


class TestParallelHtmlScraper:
    """Test ParallelHtmlScraper."""

    @staticmethod
    def test(
        mocker: MockerFixture,
        mock_aioresponse: aioresponses,
        monkeypatch: pytest.MonkeyPatch,
        resource_path_root: Path,
    ) -> None:
        """Test."""
        monkeypatch.setattr(HtmlTextLoadCoroutine, "execute", HtmlTextLoadCoroutineForSimulateProcessTime.execute)
        host_google = "https://www.google.co.jp"
        path_and_content = {
            "/webhp?tab=rw": (resource_path_root / "google_search.html").read_bytes(),
            "/imghp?hl=ja&tab=wi&ogbl": (resource_path_root / "google_image.html").read_bytes(),
            "/shopping?hl=ja&source=og&tab=wf": (resource_path_root / "google_shopping.html").read_bytes(),
            "/save": (resource_path_root / "google_collection.html").read_bytes(),
            "https://www.google.co.jp/maps": (resource_path_root / "google_maps.html").read_bytes(),
            "https://www.google.co.jp/drive/apps.html": (resource_path_root / "google_drive.html").read_bytes(),
            "https://www.google.co.jp/mail/help/intl/ja/about.html?vm=r": (
                resource_path_root / "gmail.html"
            ).read_bytes(),
        }
        for path, file_content in path_and_content.items():
            mock_aioresponse.get(
                path if host_google in path else f"{host_google}{path}",
                status=200,
                body=file_content,
            )
        spy_sleep = mocker.spy(asyncio, "sleep")
        list_response = ParallelHtmlScraper.execute(host_google, path_and_content.keys(), AnalyzerForTest())
        assert sorted(list_response) == sorted(
            [
                "Google",
                "Google 画像検索",
                "Google ショッピング",
                "コレクション",
                "Google マップ",
                f"{os.linesep}        Google ドライブ{os.linesep}    ",
                f"{os.linesep}        Gmail - Google のメール{os.linesep}    ",
            ],
        )
        spy_sleep.assert_any_call(HtmlRequestCoroutine.MINIMUM_INTERVAL_REQUEST)

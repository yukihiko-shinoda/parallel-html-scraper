"""Tests for parallel_url_scraper."""
import asyncio
import os

from bs4 import BeautifulSoup  # type: ignore

from parallelhtmlscraper.html_text_load_coroutine import HtmlTextLoadCoroutine
from parallelhtmlscraper.parallel_html_scraper import ParallelHtmlScraper
from tests.testlibraries.analyzer_for_test import AnalyzerForTest


class HtmlTextLoadCoroutineForSimulateProcessTime(HtmlTextLoadCoroutine):
    @classmethod
    async def execute(cls, response):
        await asyncio.sleep(5.1)
        return BeautifulSoup(await super()._execute(response), "html.parser")


class TestParallelHtmlScraper:
    """Test ParallelHtmlScraper."""

    @staticmethod
    def test(mocker, mock_aioresponse, monkeypatch, resource_path_root):
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
            mock_aioresponse.get(path if host_google in path else f"{host_google}{path}", status=200, body=file_content)
        mocker.spy(asyncio, "sleep")
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
            ]
        )
        # noinspection PyUnresolvedReferences
        # pylint: disable=no-member
        asyncio.sleep.assert_any_call(0.1)

import asyncio

from parallelhtmlscraper.html_text_load_coroutine import HtmlTextLoadCoroutine
from parallelhtmlscraper.parallel_html_scraper import ParallelHtmlScraper
from tests.testlibraries.analyzer_for_test import AnalyzerForTest
from tests.testlibraries.instance_resource import InstanceResource


class HtmlTextLoadCoroutineForSimulateProcessTime(HtmlTextLoadCoroutine):
    @classmethod
    async def execute(cls, response):
        await asyncio.sleep(5.1)
        from bs4 import BeautifulSoup
        return BeautifulSoup(await super()._execute(response), 'html.parser')


class TestParallelHtmlScraper:
    @staticmethod
    def test(mocker, mock_aioresponse, monkeypatch):
        monkeypatch.setattr(HtmlTextLoadCoroutine, "execute", HtmlTextLoadCoroutineForSimulateProcessTime.execute)
        host_google = 'https://www.google.co.jp'
        path_and_content = {
            '/webhp?tab=rw': InstanceResource.PATH_FILE_HTML_GOOGLE_SEARCH.read_bytes(),
            '/imghp?hl=ja&tab=wi&ogbl': InstanceResource.PATH_FILE_HTML_GOOGLE_IMAGE.read_bytes(),
            '/shopping?hl=ja&source=og&tab=wf': InstanceResource.PATH_FILE_HTML_GOOGLE_SHOPPING.read_bytes(),
            '/save': InstanceResource.PATH_FILE_HTML_GOOGLE_COLLECTION.read_bytes(),
            'https://www.google.co.jp/maps': InstanceResource.PATH_FILE_HTML_GOOGLE_MAPS.read_bytes(),
            'https://www.google.co.jp/drive/apps.html': InstanceResource.PATH_FILE_HTML_GOOGLE_DRIVE.read_bytes(),
            'https://www.google.co.jp/mail/help/intl/ja/about.html?vm=r':
                InstanceResource.PATH_FILE_HTML_GMAIL.read_bytes(),
        }
        for path, file_content in path_and_content.items():
            mock_aioresponse.get(f'{host_google}{path}', status=200, body=file_content)
        mocker.spy(asyncio, 'sleep')
        list_response = ParallelHtmlScraper.execute(f'{host_google}', path_and_content.keys(), AnalyzerForTest())
        assert list_response == [
            'Google',
            'Google 画像検索',
            'Google ショッピング',
            'コレクション',
            'Google マップ',
            '\r\n        Google ドライブ\r\n    ',
            '\r\n        Gmail - Google のメール\r\n    '
        ]
        # noinspection PyUnresolvedReferences
        # pylint: disable=no-member
        asyncio.sleep.assert_any_call(0.1)

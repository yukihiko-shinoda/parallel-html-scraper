import asyncio

import aiohttp
import pytest

from parallelhtmlscraper import HttpTimeoutError
from parallelhtmlscraper.html_request_coroutine import HtmlRequestCoroutine
from tests.testlibraries.analyzer_for_test import AnalyzerForTest
from tests.testlibraries.instance_resource import InstanceResource


class TestHtmlRequestCoroutine:
    @staticmethod
    @pytest.mark.asyncio
    async def test(monkeypatch, mock_aioresponse):
        # noinspection PyUnusedLocal
        # pylint: disable=unused-argument
        async def mock_sleep(time):
            pass
        monkeypatch.setattr(asyncio, "sleep", mock_sleep)
        url_google = 'http://www.google.co.jp/webhp?tab=rw'
        mock_aioresponse.get(
            url_google, status=200, body=InstanceResource.PATH_FILE_HTML_GOOGLE_SEARCH.read_bytes()
        )
        async with aiohttp.ClientSession() as session:
            analyze_result = await HtmlRequestCoroutine().execute(session, url_google, AnalyzerForTest())
            assert analyze_result == 'Google'

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.asyncio
    async def test_timeout_error(mock_aioresponse, tmp_path):
        url_google = 'http://www.google.co.jp/webhp?tab=rw'
        mock_aioresponse.get(url_google, status=200, exception=asyncio.TimeoutError())
        with pytest.raises(HttpTimeoutError) as error:
            async with aiohttp.ClientSession() as session:
                await HtmlRequestCoroutine().execute(session, url_google, AnalyzerForTest())
        assert str(error.value) == f'HttpTimeoutError. URL = {url_google}'

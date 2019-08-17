import pytest
from aiohttp import ClientResponse

from parallelhtmlscraper.html_text_load_coroutine import HtmlTextLoadCoroutine
from tests.conftest import AioresponseParameter
from tests.testlibraries.instance_resource import InstanceResource


class TestHtmlTextRoadCoroutine:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize('client_response', [
        AioresponseParameter(
            InstanceResource.PATH_FILE_HTML_EMOJI.read_bytes(),
            {'charset': '', 'Content-Type': 'text/html'}
        )
    ], indirect=['client_response'])
    async def test(client_response: ClientResponse):
        soup = await HtmlTextLoadCoroutine.execute(client_response)
        body = soup.find('body')
        assert body.text.strip() == 'あ💫'

import asyncio
from dataclasses import dataclass
from typing import Union, Dict, Optional

import aiohttp
import pytest
from aioresponses import aioresponses


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as mocked:
        yield mocked


@dataclass
class AioresponseParameter:
    body: Union[str, bytes]
    headers: Optional[Dict[str, str]] = None


@pytest.fixture
def client_response(mock_aioresponse, request):
    aioresponse_parameter: AioresponseParameter = request.param
    url_temporary = 'https://tsohlacol/'
    mock_aioresponse.get(
        url_temporary, status=200, body=aioresponse_parameter.body, headers=aioresponse_parameter.headers
    )

    async def coroutine():
        async with aiohttp.ClientSession() as session:
            return await session.get(url_temporary, timeout=3)
    yield asyncio.get_event_loop().run_until_complete(coroutine())

"""Configuration for pytest."""
import asyncio
from dataclasses import dataclass
from typing import Dict, Optional, Union

import aiohttp
import pytest
from aioresponses import aioresponses  # type: ignore

collect_ignore = ["setup.py"]


@pytest.fixture
def mock_aioresponse():
    with aioresponses() as mocked:
        yield mocked


@pytest.fixture
def html_byte(resource_path_root, request):
    yield resource_path_root / request.param


@dataclass
class AioresponseParameterHtmlByte:
    body: str
    headers: Optional[Dict[str, str]] = None


@dataclass
class AioresponseParameter:
    body: Union[str, bytes]
    headers: Optional[Dict[str, str]] = None


# pylint: disable=redefined-outer-name
@pytest.fixture
def client_response_html_byte(resource_path_root, request, mock_aioresponse):
    aioresponse_parameter = AioresponseParameter(
        (resource_path_root / request.param.body).read_bytes(), request.param.headers
    )
    yield from generate_client_response(mock_aioresponse, aioresponse_parameter)


# pylint: disable=redefined-outer-name
@pytest.fixture
def client_response(mock_aioresponse, request):
    yield from generate_client_response(mock_aioresponse, request.param)


# pylint: disable=redefined-outer-name
def generate_client_response(mock_aioresponse, aioresponse_parameter: AioresponseParameter):
    """Generates client responce."""
    url_temporary = "https://tsohlacol/"
    mock_aioresponse.get(
        url_temporary, status=200, body=aioresponse_parameter.body, headers=aioresponse_parameter.headers
    )

    async def coroutine():
        async with aiohttp.ClientSession() as session:
            return await session.get(url_temporary, timeout=3)

    yield asyncio.get_event_loop().run_until_complete(coroutine())

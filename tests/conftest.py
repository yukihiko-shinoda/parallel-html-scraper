"""Configuration for pytest."""

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import AsyncGenerator
from typing import Dict
from typing import Optional
from typing import Union

import aiohttp
import pytest
import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import TestServer
from aioresponses import aioresponses  # type: ignore

if TYPE_CHECKING:
    from pathlib import Path

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
@pytest_asyncio.fixture
async def client_response_html_byte(resource_path_root, request, mock_aioresponse):
    aioresponse_parameter = AioresponseParameter(
        (resource_path_root / request.param.body).read_bytes(),
        request.param.headers,
    )
    yield await generate_client_response(mock_aioresponse, aioresponse_parameter)


# pylint: disable=redefined-outer-name
@pytest_asyncio.fixture
async def client_response(mock_aioresponse, request):
    yield await generate_client_response(mock_aioresponse, request.param)


# pylint: disable=redefined-outer-name
async def generate_client_response(mock_aioresponse, aioresponse_parameter: AioresponseParameter):
    """Generates client responce."""
    url_temporary = "https://tsohlacol/"
    mock_aioresponse.get(
        url_temporary,
        status=200,
        body=aioresponse_parameter.body,
        headers=aioresponse_parameter.headers,
    )

    async with aiohttp.ClientSession() as session:
        return await session.get(url_temporary, timeout=3)


@pytest_asyncio.fixture
async def client_response_from_local_server(
    resource_path_root: "Path",
    request: pytest.FixtureRequest,
) -> AsyncGenerator[aiohttp.ClientResponse, None]:
    """Yield a real response from a local HTTP server that serves the resource file with the given headers."""
    parameter: AioresponseParameterHtmlByte = request.param
    body = (resource_path_root / parameter.body).read_bytes()

    async def handler(_request: web.Request) -> web.Response:
        return web.Response(body=body, headers=parameter.headers)

    application = web.Application()
    application.router.add_get("/", handler)
    async with TestServer(application) as server, aiohttp.ClientSession() as session, session.get(
        server.make_url("/"),
    ) as response:
        yield response

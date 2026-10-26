# Copyright (C) 2019 Yukihiko Shinoda
"""Configuration for pytest."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import aiohttp
import pytest
import pytest_asyncio
from aiohttp import web
from aiohttp.test_utils import TestServer
from aioresponses import aioresponses

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from collections.abc import Generator
    from pathlib import Path


@pytest.fixture
def mock_aioresponse() -> Generator[aioresponses, None, None]:
    with aioresponses() as mocked:
        yield mocked


@dataclass
class AioresponseParameterHtmlByte:
    body: str
    headers: dict[str, str] | None = None


# pylint: disable=redefined-outer-name
@pytest_asyncio.fixture
async def client_response_html_byte(
    resource_path_root: Path,
    request: pytest.FixtureRequest,
    mock_aioresponse: aioresponses,
) -> AsyncGenerator[aiohttp.ClientResponse, None]:
    """Yield a response mocked by aioresponses with the resource file and the given headers."""
    parameter: AioresponseParameterHtmlByte = request.param
    url_temporary = "https://tsohlacol/"
    mock_aioresponse.get(
        url_temporary,
        status=200,
        body=(resource_path_root / parameter.body).read_bytes(),
        headers=parameter.headers,
    )
    async with aiohttp.ClientSession() as session:
        yield await session.get(url_temporary, timeout=aiohttp.ClientTimeout(total=3))


@pytest_asyncio.fixture
async def client_response_from_local_server(
    resource_path_root: Path,
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

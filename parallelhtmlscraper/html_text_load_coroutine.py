# Copyright (C) 2019 Yukihiko Shinoda
"""Parser for response body to BeautifulSoup."""

from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from aiohttp import ClientResponse


class HtmlTextLoadCoroutine:
    """Parser for response body to BeautifulSoup."""

    LOGGER = getLogger(__name__)

    @classmethod
    async def execute(cls, response: ClientResponse) -> BeautifulSoup:
        return BeautifulSoup(await cls._execute(response), "html.parser")

    @classmethod
    async def _execute(cls, response: ClientResponse) -> str:
        try:
            return await response.text()
        except UnicodeDecodeError:
            # if response header includes no encoding information,
            # aiohttp try to detect encoding by chardet.
            # However chardet doesn't support Emoji.
            cls.LOGGER.exception("UnicodeDecodeError. URL = %s, encoding = %s", response.url, response.get_encoding())
        return await response.text("utf-8")

"""Parser for response body to BeautifulSoup."""
from logging import getLogger

from aiohttp import ClientResponse
from bs4 import BeautifulSoup  # type: ignore


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
        except UnicodeDecodeError as error:
            # if response header includes no encoding information,
            # aiohttp try to detect encoding by chardet.
            # However chardet doesn't support Emoji.
            # Reason: @see https://github.com/PyCQA/pylint/issues/2395 pylint: disable=logging-fstring-interpolation
            cls.LOGGER.error(f"UnicodeDecodeError. URL = {response.url}, encoding = {response.get_encoding()}")
            # Reason: @see https://github.com/PyCQA/pylint/issues/2395 pylint: disable=logging-fstring-interpolation
            cls.LOGGER.exception(f"{error}")
        return await response.text("utf-8")

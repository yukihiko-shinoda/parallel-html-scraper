"""Controlls traffic of parallel processes for HTML request."""
import asyncio
from logging import getLogger
from typing import TypeVar

from aiohttp import ClientSession

from parallelhtmlscraper.exceptions import HttpTimeoutError
from parallelhtmlscraper.html_analyzer import HtmlAnalyzer
from parallelhtmlscraper.html_text_load_coroutine import HtmlTextLoadCoroutine

# noinspection PyShadowingBuiltins
_T = TypeVar("_T")


class HtmlRequestCoroutine:
    """Controlls traffic of parallel processes for HTML request."""

    # ↓ Reason: Based on experience
    SEMAPHORE_MAX_VALUE = 5
    # ↓ Reason: Librahack incident @see https://www.google.com/search?q=Librahack%E4%BA%8B%E4%BB%B6
    MINIMUM_INTERVAL_REQUEST = 1
    # ↓ Reason: There is no load on the system and no problem for tasks.
    INTERVAL_CHECK_SEMAPHORE_LOCK = 0.1
    # ↓ Reason: Based on experience
    TIME_OUT = 30
    # ↓ Reason: Based on experience
    INTERVAL_ACCESS_TO_RESPONSE_BODY = 0.12

    def __init__(self, *, semaphore: asyncio.Semaphore = None):
        self.semaphore = asyncio.Semaphore(self.SEMAPHORE_MAX_VALUE) if semaphore is None else semaphore
        self.semaphore_for_interval = asyncio.Semaphore(1)
        self.logger = getLogger(__name__)

    async def execute(
        self,
        client_session: ClientSession,
        url: str,
        analyzer: HtmlAnalyzer[_T],
        *,
        interval: int = MINIMUM_INTERVAL_REQUEST,
    ) -> _T:
        """function want to limit the number of parallel"""
        async with self.semaphore_for_interval:
            await asyncio.sleep(interval)
            while self.semaphore.locked():
                await asyncio.sleep(self.INTERVAL_CHECK_SEMAPHORE_LOCK)
        async with self.semaphore:
            try:
                response = await client_session.get(url, timeout=self.TIME_OUT)
            except asyncio.TimeoutError as error:
                raise HttpTimeoutError(url=url) from error
            # ↓ Because response raises error when access to response body too fast
            await asyncio.sleep(self.INTERVAL_ACCESS_TO_RESPONSE_BODY)
            response.raise_for_status()
            # Reason: @see https://github.com/PyCQA/pylint/issues/2395 pylint: disable=logging-fstring-interpolation
            self.logger.info(f"status = {str(response.status)}")
            soup = await HtmlTextLoadCoroutine.execute(response)
        return await analyzer.execute(soup)

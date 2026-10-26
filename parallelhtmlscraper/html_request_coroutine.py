# Copyright (C) 2019 Yukihiko Shinoda
"""Controlls traffic of parallel processes for HTML request."""

from __future__ import annotations

import asyncio
from logging import getLogger
from typing import TYPE_CHECKING
from typing import TypeVar

from aiohttp import ClientTimeout

from parallelhtmlscraper.exceptions import HttpTimeoutError
from parallelhtmlscraper.html_text_load_coroutine import HtmlTextLoadCoroutine

if TYPE_CHECKING:
    from aiohttp import ClientSession
    from bs4 import BeautifulSoup

    from parallelhtmlscraper.html_analyzer import HtmlAnalyzer

# noinspection PyShadowingBuiltins
_T = TypeVar("_T")


class HtmlRequestCoroutine:
    """Controlls traffic of parallel processes for HTML request."""

    # ↓ Reason: Based on experience
    SEMAPHORE_MAX_VALUE = 5
    # ↓ Reason: Librahack incident @see https://www.google.com/search?q=Librahack%E4%BA%8B%E4%BB%B6
    MINIMUM_INTERVAL_REQUEST = 1
    # ↓ Reason: Based on experience
    TIME_OUT = 30
    # ↓ Reason: Based on experience
    INTERVAL_ACCESS_TO_RESPONSE_BODY = 0.12

    def __init__(self, *, semaphore: asyncio.Semaphore | None = None) -> None:
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
        """Request the URL with limiting the number of parallel requests and the interval between them."""
        await self._acquire_slot(interval)
        try:
            soup = await self._request(client_session, url)
        finally:
            self.semaphore.release()
        return await analyzer.execute(soup)

    async def _acquire_slot(self, interval: int) -> None:
        async with self.semaphore_for_interval:
            # Waits for a free slot while holding the interval lock
            # so that the next request can't start until this one has started.
            await asyncio.sleep(interval)
            await self.semaphore.acquire()

    async def _request(self, client_session: ClientSession, url: str) -> BeautifulSoup:
        try:
            response = await client_session.get(url, timeout=ClientTimeout(total=self.TIME_OUT))
        except asyncio.TimeoutError as error:
            raise HttpTimeoutError(url=url) from error
        # ↓ Because response raises error when access to response body too fast
        await asyncio.sleep(self.INTERVAL_ACCESS_TO_RESPONSE_BODY)
        response.raise_for_status()
        self.logger.info("status = %s", response.status)
        return await HtmlTextLoadCoroutine.execute(response)

"""Executes HTML requests as parallel."""
import asyncio
from typing import Iterable, List, TypeVar

import aiohttp

from parallelhtmlscraper.html_analyzer import HtmlAnalyzer
from parallelhtmlscraper.html_request_coroutine import HtmlRequestCoroutine

# noinspection PyShadowingBuiltins
_T = TypeVar("_T")


class ParallelHtmlRequestCoroutine:
    """Executes HTML requests as parallel."""

    @staticmethod
    async def execute(
        base_url: str,
        list_url: Iterable[str],
        analyzer: HtmlAnalyzer[_T],
        *,
        semaphore: asyncio.Semaphore = None,
        interval: int = HtmlRequestCoroutine.MINIMUM_INTERVAL_REQUEST,
    ) -> List[_T]:
        """Executes HTML requests as parallel."""
        semaphore = asyncio.Semaphore(HtmlRequestCoroutine.SEMAPHORE_MAX_VALUE) if semaphore is None else semaphore
        html_request_coroutine = HtmlRequestCoroutine(semaphore=semaphore)
        async with aiohttp.ClientSession() as session:
            tasks = [
                html_request_coroutine.execute(
                    session, url if base_url in url else f"{base_url}{url}", analyzer, interval=interval
                )
                for url in list_url
            ]
            return await asyncio.gather(*tasks)  # type: ignore

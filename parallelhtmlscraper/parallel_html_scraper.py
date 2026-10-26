# Copyright (C) 2019 Yukihiko Shinoda
"""API of parallel HTML scraping."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING
from typing import TypeVar

from parallelhtmlscraper.html_request_coroutine import HtmlRequestCoroutine
from parallelhtmlscraper.parallel_html_request_coroutine import ParallelHtmlRequestCoroutine

if TYPE_CHECKING:
    from collections.abc import Iterable

    from parallelhtmlscraper.html_analyzer import HtmlAnalyzer

__all__ = ["ParallelHtmlScraper"]
# noinspection PyShadowingBuiltins
_T = TypeVar("_T")


class ParallelHtmlScraper:
    """API of parallel HTML scraping.

    Following steps hasn't implemented:
    - don't follow link when a tag has rel="nofollow"
    - Follow attributes of robots meta tag
    - Follow X-Robots-Tag in HTTP header
    - Follow robots.txt
    - Set User-agent and etc...
    @see https://vaaaaaanquish.hatenablog.com/entry/2017/12/01/064227
    """

    @staticmethod
    def execute(
        base_url: str,
        list_url: Iterable[str],
        analyzer: HtmlAnalyzer[_T],
        *,
        limit: int = HtmlRequestCoroutine.SEMAPHORE_MAX_VALUE,
        interval: int = HtmlRequestCoroutine.MINIMUM_INTERVAL_REQUEST,
    ) -> list[_T]:
        """Execute parallel HTML scraping."""
        return asyncio.run(ParallelHtmlScraper._execute(base_url, list_url, analyzer, limit=limit, interval=interval))

    @staticmethod
    async def _execute(
        base_url: str,
        list_url: Iterable[str],
        analyzer: HtmlAnalyzer[_T],
        *,
        limit: int,
        interval: int,
    ) -> list[_T]:
        # Reason: Before Python 3.10, asyncio.Semaphore binds the event loop when instantiated,
        # so it has to be instantiated in the event loop which asyncio.run() creates.
        return await ParallelHtmlRequestCoroutine.execute(
            base_url,
            list_url,
            analyzer,
            semaphore=asyncio.Semaphore(limit),
            interval=interval,
        )

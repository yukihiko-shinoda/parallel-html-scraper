"""API of parallel HTML scraping."""
import asyncio
from typing import Iterable, List, TypeVar

from parallelhtmlscraper.html_analyzer import HtmlAnalyzer
from parallelhtmlscraper.html_request_coroutine import HtmlRequestCoroutine
from parallelhtmlscraper.parallel_html_request_coroutine import ParallelHtmlRequestCoroutine

__all__: List[str] = ["ParallelHtmlScraper"]
# noinspection PyShadowingBuiltins
_T = TypeVar("_T")


class ParallelHtmlScraper:
    """
    API of parallel HTML scraping.
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
        interval: int = HtmlRequestCoroutine.MINIMUM_INTERVAL_REQUEST
    ) -> List[_T]:
        """Executes parallel HTML scraping."""
        return asyncio.get_event_loop().run_until_complete(
            ParallelHtmlRequestCoroutine.execute(
                base_url, list_url, analyzer, semaphore=asyncio.Semaphore(limit), interval=interval
            )
        )

import asyncio
from typing import List, Iterable, TypeVar

from parallelhtmlscraper.html_request_coroutine import HtmlRequestCoroutine
from parallelhtmlscraper.parallel_html_request_coroutine import ParallelHtmlRequestCoroutine
from parallelhtmlscraper.html_analyzer import HtmlAnalyzer
__all__: List[str] = ['ParallelHtmlScraper']
# noinspection PyShadowingBuiltins
_T = TypeVar('_T')


class ParallelHtmlScraper:
    # @see https://vaaaaaanquish.hatenablog.com/entry/2017/12/01/064227
    # TODO aタグにrel="nofollow"が設定されていたら辿らない
    # TODO robots metaタグの属性記載に従う
    # TODO HTTP ヘッダーのX-Robots-Tagに従う
    # TODO robots.txtに従う
    # TODO User-agentなどを正しく設定する
    @staticmethod
    def execute(
            base_url: str, list_url: Iterable[str], analyzer: HtmlAnalyzer[_T],
            *,
            limit: int = HtmlRequestCoroutine.SEMAPHORE_MAX_VALUE,
            interval: int = HtmlRequestCoroutine.MINIMUM_INTERVAL_REQUEST
    ) -> List[_T]:
        return asyncio.get_event_loop().run_until_complete(
            ParallelHtmlRequestCoroutine.execute(
                base_url, list_url, analyzer, semaphore=asyncio.Semaphore(limit), interval=interval
            )
        )

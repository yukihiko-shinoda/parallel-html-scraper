"""Helps to scrape html file."""
from typing import List

from parallelhtmlscraper.exceptions import *  # noqa
from parallelhtmlscraper.html_analyzer import *  # noqa
from parallelhtmlscraper.parallel_html_scraper import *  # noqa

__version__ = "0.1.0"

__all__: List[str] = []
# pylint: disable=undefined-variable
__all__ += exceptions.__all__  # type: ignore # noqa
__all__ += html_analyzer.__all__  # type: ignore # noqa
__all__ += parallel_html_scraper.__all__  # type: ignore # noqa

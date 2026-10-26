# Copyright (C) 2019 Yukihiko Shinoda
"""Helps to scrape html file."""

from parallelhtmlscraper.exceptions import Error
from parallelhtmlscraper.exceptions import HttpTimeoutError
from parallelhtmlscraper.html_analyzer import HtmlAnalyzer
from parallelhtmlscraper.parallel_html_scraper import ParallelHtmlScraper

__version__ = "0.1.0"

__all__ = ["Error", "HtmlAnalyzer", "HttpTimeoutError", "ParallelHtmlScraper"]

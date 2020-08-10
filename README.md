# Parallel HTML Scraper

[![Test](https://github.com/yukihiko-shinoda/parallel-html-scraper/workflows/Test/badge.svg)](https://github.com/yukihiko-shinoda/parallel-html-scraper/actions?query=workflow%3ATest)
[![Test Coverage](https://api.codeclimate.com/v1/badges/5f07cb148a0770db4be4/test_coverage)](https://codeclimate.com/github/yukihiko-shinoda/parallel-html-scraper/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/5f07cb148a0770db4be4/maintainability)](https://codeclimate.com/github/yukihiko-shinoda/parallel-html-scraper/maintainability)
[![Code Climate technical debt](https://img.shields.io/codeclimate/tech-debt/yukihiko-shinoda/parallel-html-scraper)](https://codeclimate.com/github/yukihiko-shinoda/parallel-html-scraper)
[![Updates](https://pyup.io/repos/github/yukihiko-shinoda/parallel-html-scraper/shield.svg)](https://pyup.io/repos/github/yukihiko-shinoda/parallel-html-scraper/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/parallelhtmlscraper)](https://pypi.org/project/parallelhtmlscraper/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/parallelhtmlscraper)](https://pypi.org/project/parallelhtmlscraper/)
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fyukihiko-shinoda%2Fparallel-html-scraper)](http://twitter.com/share?text=Parallel%20HTML%20Scraper&url=https://pypi.org/project/parallelhtmlscraper/&hashtags=python)

Helps you to web scrape html file in parallel without async / await syntax.

## Feature

This project helps you to web scrape html file in parallel without async / await syntax.

## Installation

```console
pip install parallelhtmlscraper
```

## Usage

Minimum example:

```python
from bs4 import BeautifulSoup

from parallelhtmlscraper.html_analyzer import HtmlAnalyzer
from parallelhtmlscraper.parallel_html_scraper import ParallelHtmlScraper

class AnalyzerForTest(HtmlAnalyzer):
    async def execute(self, soup: BeautifulSoup) -> str:
        return soup.find('title').text

host_google = 'https://www.google.com'
path_and_content = [
    '',                                                           # Google Search
    '/imghp?hl=EN',                                               # Google Images
    '/shopping?hl=en',                                            # Google Shopping
    '/save',                                                      # Collection
    'https://www.google.com/maps?hl=en',                          # Google Maps
    'https://www.google.com/drive/apps.html',                     # Google drive
    'https://www.google.com/mail/help/intl/en/about.html?vm=r',   # GMail
]

list_response = ParallelHtmlScraper.execute(host_google, path_and_content, AnalyzerForTest())
print(list_response)
```

```console
$ pipenv run python test.py
['\n      Gmail - Email from Google\n    ', 'Google Images', '  Google Maps  ', 'Using Google Drive - New Features, Benefits & Advantages of Google Cloud Storage', 'Google Shopping', 'Google', 'Collections']
```

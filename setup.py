#!/usr/bin/env python
"""This module implements build settings."""

from setuptools import setup
from setuptools import find_packages


def main():
    """This function implements build settings."""
    with open('README.md', 'r', encoding='utf8') as file:
        readme = file.read()

    setup(
        name='parallelhtmlscraper',
        version='0.0.0',
        description='This project helps you to web scrape html file.',
        long_description=readme,
        long_description_content_type='text/markdown',
        author='Yukihiko Shinoda',
        author_email='yuk.hik.future@gmail.com',
        packages=find_packages(exclude=("tests*",)),
        package_data={"parallelhtmlscraper": ["py.typed"]},
        install_requires=[
            'aiohttp',
            'beautifulsoup4',
        ],
        url="https://github.com/yukihiko-shinoda/parallel-media-downloader",
        keywords="parallel HTML web scraping scrape aiohttp beautifulsoup beautifulsoup4",
    )


if __name__ == '__main__':
    main()

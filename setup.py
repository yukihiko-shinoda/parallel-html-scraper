#!/usr/bin/env python
"""This module implements build settings."""

from setuptools import find_packages, setup  # type: ignore


def main():
    """This function implements build settings."""
    with open("README.md", "r", encoding="utf8") as file:
        readme = file.read()

    setup(
        author="Yukihiko Shinoda",
        author_email="yuk.hik.future@gmail.com",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Information Technology",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: System :: Archiving",
            "Topic :: Text Processing :: Markup :: HTML",
            "Typing :: Typed",
        ],
        dependency_links=[],
        description="This project helps you to web scrape html file.",
        install_requires=["aiohttp", "beautifulsoup4"],
        keywords="parallel HTML web scraping scrape aiohttp beautifulsoup beautifulsoup4",
        long_description=readme,
        long_description_content_type="text/markdown",
        name="parallelhtmlscraper",
        packages=find_packages(exclude=("tests*",)),
        package_data={"parallelhtmlscraper": ["py.typed"]},
        setup_requires=["pytest-runner"],
        url="https://github.com/yukihiko-shinoda/parallel-media-downloader",
        version="0.0.0",
    )


if __name__ == "__main__":
    main()

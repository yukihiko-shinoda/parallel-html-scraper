#!/usr/bin/env python
"""This module implements build settings."""

from setuptools import find_packages, setup  # type: ignore


def main():
    """This function implements build settings."""
    with open("README.md", "r", encoding="utf8") as file:
        readme = file.read()

    setup(
        name="parallelhtmlscraper",
        version="0.0.0",
        description="This project helps you to web scrape html file.",
        long_description=readme,
        long_description_content_type="text/markdown",
        author="Yukihiko Shinoda",
        author_email="yuk.hik.future@gmail.com",
        packages=find_packages(exclude=("tests*",)),
        package_data={"parallelhtmlscraper": ["py.typed"]},
        install_requires=["aiohttp", "beautifulsoup4"],
        dependency_links=[],
        setup_requires=["pytest-runner"],
        url="https://github.com/yukihiko-shinoda/parallel-media-downloader",
        keywords="parallel HTML web scraping scrape aiohttp beautifulsoup beautifulsoup4",
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
    )


if __name__ == "__main__":
    main()

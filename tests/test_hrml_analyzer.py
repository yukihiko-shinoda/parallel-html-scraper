# Copyright (C) 2019 Yukihiko Shinoda
"""Test for html_analyzer."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from bs4 import BeautifulSoup

from parallelhtmlscraper import HtmlAnalyzer

if TYPE_CHECKING:
    from pathlib import Path


class SampleHtmlAnalyzer(HtmlAnalyzer[object]):
    async def execute(self, soup: BeautifulSoup) -> object:
        return await super().execute(soup)


class TestHtmlAnalyzer:
    """Test for HtmlAnalyzer."""

    @staticmethod
    @pytest.mark.asyncio
    async def test(resource_path_root: Path) -> None:
        """Tests."""
        with pytest.raises(NotImplementedError):
            await SampleHtmlAnalyzer().execute(
                BeautifulSoup((resource_path_root / "google_search.html").read_bytes(), "html.parser"),
            )

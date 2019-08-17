"""This module implements fixture of instance."""
from pathlib import Path


class InstanceResource:
    """This class implements fixture of instance."""
    PATH_TESTS: Path = Path(__file__).parent.parent
    PATH_TEST_RESOURCES: Path = PATH_TESTS / 'testresources'
    PATH_FILE_CONFIG_FOR_TEST: Path = PATH_TEST_RESOURCES / 'config.yml'
    PATH_FILE_HTML_GOOGLE_SEARCH: Path = PATH_TEST_RESOURCES / 'google_search.html'
    PATH_FILE_HTML_GOOGLE_IMAGE: Path = PATH_TEST_RESOURCES / 'google_image.html'
    PATH_FILE_HTML_GOOGLE_SHOPPING: Path = PATH_TEST_RESOURCES / 'google_shopping.html'
    PATH_FILE_HTML_GOOGLE_COLLECTION: Path = PATH_TEST_RESOURCES / 'google_collection.html'
    PATH_FILE_HTML_GOOGLE_MAPS: Path = PATH_TEST_RESOURCES / 'google_maps.html'
    PATH_FILE_HTML_GOOGLE_DRIVE: Path = PATH_TEST_RESOURCES / 'google_drive.html'
    PATH_FILE_HTML_GMAIL: Path = PATH_TEST_RESOURCES / 'gmail.html'
    PATH_FILE_HTML_EMOJI: Path = PATH_TEST_RESOURCES / 'emoji.html'

import os.path
import logging
from bs4 import BeautifulSoup
from .read_html_file import read_html_file
from .read_markdown_file import read_markdown_file


class UnsupportedFileExtension(Exception):
    def __init__(self, *args):
        super().__init__("Unsupported file extension", *args)


def read_file_to_soup(input_file: str) -> str:

    log = logging.getLogger(__name__)

    # Extract file extension from input_file
    _, file_extension = os.path.splitext(input_file)

    # Determine the file type based on the first letter of the file extension
    match file_extension[1].lower() if file_extension else "":
        case "x" | "h":
            html = read_html_file(input_file)
        case "m":
            html = read_markdown_file(input_file)
        case _:
            raise UnsupportedFileExtension(file_extension)

    # Try to parse to soup
    log.info("Parsing to beautiful soup")
    return BeautifulSoup(html, "html.parser")

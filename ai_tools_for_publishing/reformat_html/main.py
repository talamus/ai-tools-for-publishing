import os.path
from typing import Any, Dict
import logging
from bs4 import BeautifulSoup
from .read_html_file import read_html_file
from .write_soup_to_file import write_soup_to_file


def main(cfg: Dict[str, Any]) -> None:
    """Reads HTML files and writes them back in reformatted form."""

    log = logging.getLogger(__name__)

    input_files = cfg.get("input_files")
    output_path = cfg.get("output_path")

    # If the output path is set, make sure it is a directory
    if output_path:
        if not os.path.isdir(output_path):
            raise FileNotFoundError(f"'{output_path}' is not a directory")
        log.info("Writing to directory %s...", output_path)

    # The main loop
    for input_file in input_files:

        # Read the HTML file into a BeautifulSoup object
        try:
            html = read_html_file(input_file)
            soup = BeautifulSoup(html, "html.parser")
        except Exception as error:
            log.error(
                "Error while reading HTML file",
                extra={"file": input_file, "error": str(error)},
            )
            continue

        # Write the soup to a file
        try:
            write_soup_to_file(input_file, soup, cfg)
        except Exception as error:
            log.error(
                "Error while writing HTML file",
                extra={"file": input_file, "error": str(error)},
            )
            continue

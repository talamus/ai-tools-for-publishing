import os.path
from typing import Any, Dict
import logging
from bs4 import BeautifulSoup
from ai_tools_for_publishing.reformat_text import (
    read_file_to_soup,
    get_body_from_soup,
    write_soup_to_file,
)
from ai_tools_for_publishing.utils import read_yaml_file_to_dict
from .list_unknown_words import collect_unknown_words, print_unknown_words
from .hyphenate_body import hyphenate_body


def main(cfg: Dict[str, Any]) -> None:
    """Read multiple HTML or Markdown documents and hyphenate them."""

    log = logging.getLogger(__name__)

    input_files = cfg.get("input_files")
    output_path = cfg.get("output_path")

    # If the output path is set, make sure it is a directory
    if output_path:
        if not os.path.isdir(output_path):
            raise FileNotFoundError(f"'{output_path}' is not a directory")
        log.info("Writing to directory %s...", output_path)

    # If we have a file of known hyphenations, load it
    known_hyphenations = dict()
    if cfg["hyphenations_file"]:
        known_hyphenations = read_yaml_file_to_dict(cfg["hyphenations_file"])
        log.debug(
            "Loaded known hyphenations from %s",
            cfg["hyphenations_file"],
            extra={"hyphenations": known_hyphenations},
        )

    # The main loop
    for input_file in input_files:

        # Read the file into a BeautifulSoup object and find the body
        try:
            soup = read_file_to_soup(input_file)
            body = get_body_from_soup(soup)
        except Exception as error:
            log.error(
                "Error while reading %s",
                input_file,
                extra={"error": str(error)},
            )
            continue

        # If we are collecting unknown hyphenations, do that and continue
        if cfg["list_unknown"]:
            log.info("Collecting unknown words from %s...", input_file)
            collect_unknown_words(body)
            continue

        # Otherwise, hyphenate the body
        else:
            log.info("Hyphenating %s...", input_file)
            hyphenate_body(body, known_hyphenations, cfg)

        # Write the soup to a file
        write_soup_to_file(input_file, soup, cfg)

    # If we were collecting unknown words, print them to STDOUT
    if cfg["list_unknown"]:
        print_unknown_words()

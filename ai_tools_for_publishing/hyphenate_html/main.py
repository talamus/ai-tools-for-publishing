import os.path
from typing import Any, List, Dict, Optional
import logging
import yaml
from bs4 import BeautifulSoup
from ai_tools_for_publishing.html_to_xhtml import write_xhtml_file
from .default_config import DEFAULT_CONFIG
from .list_unknown_words import collect_unknown_words, print_unknown_words
from .hyphenate_body import hyphenate_body


def main(cfg: Dict[str, Any]) -> None:
    """Read multiple HTML documents and hyphenate them."""

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
        with open(cfg["hyphenations_file"], "r") as file:
            known_hyphenations = yaml.safe_load(file)
            if not isinstance(known_hyphenations, dict):
                raise TypeError("Known hyphenations file does not contain a dictionary")
            log.debug(
                "Loaded known hyphenations file",
                extra={"hyphenations": known_hyphenations},
            )

    # The main loop
    for input_file in input_files:

        # Read the HTML file and find the <body> from the soup
        try:
            with open(input_file) as file:
                soup = BeautifulSoup(file.read(), "html.parser")
                body = soup.find("body")
                if not body:
                    raise SyntaxError("No <body> tag")
        except Exception as error:
            log.error(
                "Error while reading HTML file",
                extra={"file": input_file, "error": str(error)},
            )
            continue

        # If we are collecting unknown hyphenations, do that and continue
        if cfg["list_unknown"]:
            log.info("Collecting unknown words from %s...", input_file)
            collect_unknown_words(body, cfg)
            continue

        # Otherwise, hyphenate the body
        else:
            log.info("Hyphenating %s...", input_file)
            hyphenate_body(body, known_hyphenations, cfg)

        # Try to find out where to write the output...
        if output_path:
            file_name = os.path.splitext(os.path.split(input_file)[1])[0]
            output_file = os.path.join(output_path, file_name + cfg["output_ext"])
        else:
            output_file = os.path.splitext(input_file)[0] + cfg["output_ext"]

        # If were are not allowed to overwrite an existing file, log the error and continue
        if os.path.exists(output_file) and not cfg["overwrite"]:
            log.error(
                "File already exists and %s is not set",
                "--overwrite",
                extra={"file": output_file},
            )
            continue

        # If we are in dry run mode, just say what would have been done and continue
        if cfg["dry_run"]:
            log.info(
                "A %s file called %s would have been written...",
                "XHTML" if cfg["output_xhtml"] else "HTML",
                output_file,
            )
            continue

        # Write the output file in either HTML or XHTML format
        if cfg["output_xhtml"]:
            write_xhtml_file(output_file, soup, cfg)
        else:
            with open(output_file, "w") as file:
                file.write(str(soup))

        # Log the success, proceed to the next file
        log.info(
            "Hyphenated %s written to %s",
            "XHTML" if cfg["output_xhtml"] else "HTML",
            output_file,
        )

    # If we were collecting unknown words, print them to STDOUT
    if cfg["list_unknown"]:
        print_unknown_words()

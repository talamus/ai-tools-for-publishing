import os.path
import logging
import yaml
from bs4 import BeautifulSoup
from .default_config import DEFAULT_CONFIG
from .list_unknown_words import collect_unknown_words, print_unknown_words
from .hyphenate_body import hyphenate_body
from .write_xhtml_file import write_xhtml_file


def hyphenate_html(
    input_files: list[str], output_path: str | None, cfg: dict = None
) -> None:
    """Hyphenate a HTML document.
    This function can be directly called.
    """

    known_hyphenations = dict()

    if cfg is None:
        cfg = dict(DEFAULT_CONFIG)
    log = logging.getLogger(__name__)

    log.debug("Configuration", extra={"cfg": cfg})

    if output_path:
        if not os.path.isdir(output_path):
            raise FileNotFoundError(f"'{output_path}' is not a directory")
        log.info("Writing to directory %s...", output_path)

    if cfg["hyphenations_file"]:
        with open(cfg["hyphenations_file"], "r") as file:
            known_hyphenations = yaml.safe_load(file)
            if not isinstance(known_hyphenations, dict):
                raise TypeError("Known hyphenations file does not contain a dictionary")
            log.debug(
                "Loaded known hyphenations file",
                extra={"hyphenations": known_hyphenations},
            )

    for input_file in input_files:
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

        if cfg["list_unknown"]:
            collect_unknown_words(input_file, body, cfg)
            continue
        else:
            hyphenate_body(input_file, body, known_hyphenations, cfg)

        if output_path:
            file_name = os.path.splitext(os.path.split(input_file)[1])[0]
            output_file = os.path.join(
                output_path, file_name + cfg["output_file_extension"]
            )
        else:
            output_file = os.path.splitext(input_file)[0] + cfg["output_file_extension"]

        if os.path.exists(output_file) and not cfg["overwrite"]:
            log.error(
                "File already exists and %s is not set",
                "--overwrite",
                extra={"file": output_file},
            )
            continue

        if cfg["dryrun"]:
            log.info(
                "A %s file called %s would have been written...",
                "XHTML" if cfg["output_xhtml"] else "HTML",
                output_file,
            )
        else:
            if cfg["output_xhtml"]:
                write_xhtml_file(output_file, soup, cfg)
            else:
                with open(output_file, "w") as file:
                    file.write(str(soup))

            log.info(
                "Hyphenated %s written to %s",
                "XHTML" if cfg["output_xhtml"] else "HTML",
                output_file,
            )

    if cfg["list_unknown"]:
        print_unknown_words()

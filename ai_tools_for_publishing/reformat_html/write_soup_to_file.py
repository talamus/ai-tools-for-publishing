import logging
import os.path
from datetime import date, datetime
from bs4 import BeautifulSoup
from .formats import FORMATS, match_str_to_format
from typing import Dict, Any

# Variables used for templating the file name and content
templating_variables: Dict[str, str] = None


def get_templating_variables(
    input_file: str, format: Dict[str, Any], cfg: Dict[str, Any]
) -> Dict[str, str]:
    """
    Get the templating variables (creating them if necessary).

    :param input_file: The path to the input file.
    :param format: A dictionary containing format information, including the file extension.
    :param cfg: A dictionary containing configuration values.
    :return: A dictionary of templating variables.
    """
    log = logging.getLogger(__name__)

    global templating_variables
    if not templating_variables:
        templating_variables = {
            "ext": format["extension"],
            "date": date.today().isoformat(),
            "time": datetime.now().strftime("%H%M%S"),
        }

        # Filter out everything but simple strings
        # or strings that look like templates
        filtered_cfg = {
            k: v
            for k, v in cfg.items()
            if isinstance(v, str)
            and ("template" in k or all(c.isalnum() or c in " '._-" for c in v))
        }

        templating_variables.update(filtered_cfg)
        log.debug(
            "Available variables for templating",
            extra={"variables": templating_variables},
        )

    templating_variables["name"] = os.path.splitext(os.path.split(input_file)[1])[0]
    return templating_variables


def get_output_file_name(
    input_file: str, format: Dict[str, Any], cfg: Dict[str, Any]
) -> str:
    """Get the output file name from the configuration and the input file."""
    log = logging.getLogger(__name__)

    try:
        templating_variables = get_templating_variables(input_file, format, cfg)
        output_file = cfg["output_name"].format(**templating_variables)
    except KeyError as error:
        raise KeyError(f"Unknown key in output_name '{cfg['output_name']}': {error}")

    output_path = cfg.get("output_path")
    if output_path:
        if not os.path.isdir(output_path):
            raise FileNotFoundError(f"'{output_path}' is not a directory")
        return os.path.join(output_path, output_file)

    return output_file


def write_soup_to_file(input_file, soup: BeautifulSoup, cfg: Dict[str, Any]) -> None:
    """Write a BeautifulSoup object to a file according to the configuration."""
    log = logging.getLogger(__name__)

    format = match_str_to_format(cfg["output_format"])
    templating_variables = get_templating_variables(input_file, format, cfg)
    output_file = get_output_file_name(input_file, format, cfg)
    content = format["formatter"](soup, templating_variables, cfg)

    # If were are not allowed to overwrite an existing file, log the error and continue
    if os.path.exists(output_file) and not cfg["overwrite"]:
        log.error(
            "File already exists and %s is not set",
            "--overwrite",
            extra={"file": output_file},
        )
        return

    # If we are in dry run mode, just say what would have been done and continue
    if cfg["dry_run"]:
        log.info(
            f"{format['description']} called %s would have been written...", output_file
        )
        return

    with open(output_file, "w") as file:
        file.write(content)
        log.info(f"{format['description']} written to %s", output_file)

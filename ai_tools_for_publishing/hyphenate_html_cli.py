import sys
import os.path
import textwrap
import argparse
import yaml
import platformdirs

from ai_tools_for_publishing.cli import main, VERBOSITY
from ai_tools_for_publishing.hyphenate_html import DEFAULT_CONFIG, hyphenate_html

__package__ = "ai_tools_for_publishing"
APP_NAME = "hyphenate_html"
APP_DESCRIPTION = f"""
Hyphenate a HTML document with BeautifulSoup and Voikko.
"""
CLI_CONFIG = {
    "config_file": os.path.join(
        platformdirs.user_config_dir(__package__), f"{APP_NAME}.config"
    ),
    "verbosity": "WARNING",
    "log_file": os.path.join(platformdirs.user_log_dir(__package__), f"{APP_NAME}.log"),
    "log_file_format": "%(asctime)s %(levelname)s %(name)s %(message)s",
    "log_level": "INFO",
    "log_max_bytes": 1000 * 1024,
    "log_max_files": 10,
}
cfg = DEFAULT_CONFIG | CLI_CONFIG
APP_USAGE = f"""
Default configuration:
{textwrap.indent(yaml.dump(cfg, sort_keys=False), "  ")}
"""


def hyphenate_html_cli():
    argparser = argparse.ArgumentParser(
        prog=f"poetry run {APP_NAME}",
        description=APP_DESCRIPTION,
        epilog=APP_USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    argparser.add_argument(
        "input_files",
        metavar="input.html",
        nargs="+",
        help="HTML documents to be processed",
    )
    argparser.add_argument(
        "-O",
        "--output-dir",
        dest="output_path",
        metavar="DIR",
        nargs=1,
        help="output directory for hyphenated HTML documents",
    )
    argparser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        default=0,
        help="set output verbosity (-v = WARNING, -vv = INFO, -vvv = DEBUG)",
    )
    argparser.add_argument(
        "-q",
        "--quiet",
        dest="verbosity",
        action="store_const",
        const=-1,
        help="Do not output anything",
    )
    argparser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="overwrite already existing HTML file",
    )
    argparser.add_argument(
        "-a",
        "--allow-unknown",
        dest="allow_unknown",
        action="store_true",
        help="hyphenate even unknown words (Use with care!)",
    )
    argparser.add_argument(
        "-l",
        "--list-unknown",
        dest="list_unknown",
        action="store_true",
        help="list unknown words and their guessed hyphenations (Dryrun implied)",
    )
    argparser.add_argument(
        "-k",
        "--known-hyphenations",
        dest="hyphenations_file",
        metavar="HYPHENATIONS.yaml",
        help="read known hyphenations from this file (YAML format)",
    )
    argparser.add_argument(
        "--output-ext",
        dest="output_file_extension",
        metavar=".EXT",
        help="file extension for hyphenated files (Default: _hyphenated.html)",
    )
    argparser.add_argument(
        "--output-xhtml",
        dest="output_xhtml",
        action="store_true",
        help="write output files in XHTML format",
    )
    argparser.add_argument(
        "--config",
        dest="alterative_config_file",
        metavar="CONFIG.yaml",
        help="read configuration from this file (YAML format)",
    )
    argparser.add_argument(
        "--loglevel",
        dest="log_level",
        metavar="LEVEL",
        choices=VERBOSITY.keys(),
        help=f"set logging level ({ ', '.join(list(VERBOSITY.keys())) })",
    )
    argparser.add_argument(
        "--dryrun",
        action="store_true",
        help="do not do anything",
    )

    args = vars(argparser.parse_args())

    # Remove arguments that are not set,
    # so that they don't override the .config file:
    args = {name: value for name, value in args.items() if value}

    sys.exit(
        main(
            lambda cfg: hyphenate_html(
                args["input_files"], args.get("output_path", [None])[0], cfg=cfg
            ),
            args,
            cfg,
            f"Starting {APP_NAME}...",
        )
    )


if __name__ == "__main__":
    hyphenate_html_cli()

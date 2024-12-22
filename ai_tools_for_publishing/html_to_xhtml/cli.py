import sys
import os.path
import textwrap
import argparse
import platformdirs
from ai_tools_for_publishing.cli import set_up_and_run, dict_to_yaml_str, VERBOSITY
from . import *


### PROGRAM INFO ##############################################################


__package__ = "ai_tools_for_publishing"
APP_NAME = "html_to_xhtml"
APP_DESCRIPTION = f"""
Convert HTML documents to XHTML.
"""
CLI_CONFIG = {
    "config_file": os.path.join(
        platformdirs.user_config_dir(__package__), f"{APP_NAME}.config"
    ),
    "verbosity": "WARNING",
    "log_file": os.path.join(platformdirs.user_log_dir(__package__), f"{APP_NAME}.log"),
    "log_file_format": "%(asctime)s %(levelname)s %(name)s %(message)s",
    "log_level": "NONE",
    "log_max_bytes": 1000 * 1024,
    "log_max_files": 10,
}
default_cfg = DEFAULT_CONFIG | CLI_CONFIG
APP_USAGE = f"""
Default configuration:
{textwrap.indent(dict_to_yaml_str(default_cfg), "  ")}
"""


### COMMAND LINE INTERFACE ####################################################


def cli():
    argparser = argparse.ArgumentParser(
        prog=APP_NAME,
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
        "-v",
        "--verbosity",
        action="count",
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
        "-O",
        "--output-path",
        dest="output_path",
        metavar="PATH",
        help="output directory for hyphenated HTML documents",
    )
    argparser.add_argument(
        "--out",
        "--output",
        dest="output_path",
        metavar="PATH",
        help=argparse.SUPPRESS,
    )
    argparser.add_argument(
        "--output-ext",
        dest="output_ext",
        metavar=".EXT",
        help=f"file extension for hyphenated files (Default: {default_cfg['output_ext']})",
    )
    argparser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="overwrite already existing files",
    )
    argparser.add_argument(
        "--config",
        dest="config_file",
        metavar="CONFIG.yaml",
        help="read configuration from this file (YAML format)",
    )
    argparser.add_argument(
        "--log-level",
        dest="log_level",
        metavar="LEVEL",
        choices=VERBOSITY.keys(),
        help=f"set logging level ({ ', '.join(list(VERBOSITY.keys())) }) (Default: {default_cfg['log_level']})",
    )
    argparser.add_argument(
        "--loglevel",
        dest="log_level",
        choices=VERBOSITY.keys(),
        help=argparse.SUPPRESS,
    )
    argparser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="do not do anything",
    )
    argparser.add_argument(
        "--dryrun",
        dest="dry_run",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args_cfg = vars(argparser.parse_args())

    # Remove arguments that are not set,
    # so that they don't override the .config file
    args_cfg = {name: value for name, value in args_cfg.items() if value}

    # Run the main program
    sys.exit(set_up_and_run(APP_NAME, main, default_cfg, args_cfg))


if __name__ == "__main__":
    cli()

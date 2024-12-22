import sys
import os.path
import textwrap
import argparse
import yaml
import platformdirs

from ai_tools_for_publishing.cli import set_up_and_run, VERBOSITY
from ai_tools_for_publishing.html_to_markdown import DEFAULT_CONFIG, html_to_markdown

__package__ = "ai_tools_for_publishing"
APP_NAME = "html_to_markdown"
APP_DESCRIPTION = f"""
Convert a HTML document to a very plain Markdown file.
Only a very limited set of HTML tags are allowed:
  <h1> <h2> <h3> <h4> <h5>
  <p> <blockquote>
  <hr>
And within these tags:
  <em> <i> <strong> <b>
  <br>
"""
CLI_CONFIG = {
    "config_file": os.path.join(
        platformdirs.user_config_dir(__package__), f"{APP_NAME}.config"
    ),
    "verbosity": "ERROR",
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


def html_to_markdown_cli():
    argparser = argparse.ArgumentParser(
        prog=f"poetry run {APP_NAME}",
        description=APP_DESCRIPTION,
        epilog=APP_USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    argparser.add_argument(
        "in_file",
        metavar="document.html",
        nargs=1,
        help="HTML file to be processed",
    )
    argparser.add_argument(
        "out_file",
        metavar="document.md",
        nargs="?",
        help="Markdown file to be written",
    )
    argparser.add_argument(
        "-v",
        "--verbosity",
        action="count",
        default=0,
        help="set output verbosity (-v = INFO, -vv = DEBUG)",
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
        help="overwrite already existing Markdown file",
    )
    argparser.add_argument(
        "--config",
        dest="alterative_config_file",
        metavar="CONFIG",
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
    args["in_file"] = args["in_file"][0]

    # Remove arguments that are not set,
    # so that they don't override the .config file:
    if not args["overwrite"]:
        del args["overwrite"]
    if not args["log_level"]:
        del args["log_level"]
    if not args["dryrun"]:
        del args["dryrun"]

    sys.exit(
        set_up_and_run(
            lambda cfg: html_to_markdown(args["in_file"], args["out_file"], cfg=cfg),
            cfg,
            args,
            f"Starting {APP_NAME}...",
        )
    )


if __name__ == "__main__":
    html_to_markdown_cli()

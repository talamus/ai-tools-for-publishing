import os.path
import argparse
import platformdirs
from ai_tools_for_publishing.cli import set_up_and_run_application, VERBOSITY
from ai_tools_for_publishing.utils import dict_to_yaml_str
from ai_tools_for_publishing.reformat_text import (
    DEFAULT_CONFIG as REFORMAT_HTML_DEFAULT_CONFIG,
    FORMATS,
)
from .default_config import DEFAULT_CONFIG
from .main import main

# fmt: off
# -----------------------------------------------------------------------------

(PARENT_NAME, APP_NAME) = __package__.split(".")
APP_DESCRIPTION = """
Hyphenate Finnish HTML documents using BeautifulSoup and Voikko.
"""
CLI_CONFIG = {
    "config_file": os.path.join(
        platformdirs.user_config_dir(PARENT_NAME), f"{APP_NAME}.config"
    ),
    "verbosity": "WARNING",
    "log_file": os.path.join(platformdirs.user_log_dir(PARENT_NAME), f"{APP_NAME}.log"),
    "log_file_format": "%(asctime)s %(levelname)s %(name)s %(message)s",
    "log_level": "NONE",
    "log_max_bytes": 1000 * 1024,
    "log_max_files": 10,
}
APP_CFG = REFORMAT_HTML_DEFAULT_CONFIG | DEFAULT_CONFIG | CLI_CONFIG
APP_USAGE = f"""
default configuration:
---
{dict_to_yaml_str(APP_CFG)}
"""
APP_CLI_ARGUMENTS = (
(("input_files",                ),{ "nargs": "+",                "metavar": "input.[html|md]",   "help": "HTML or Markdown documents to be processed", }),
(("-v",      "--verbosity",     ),{ "dest": "verbosity",         "action": "count",              "help": "set output verbosity (-v = WARNING, -vv = INFO, -vvv = DEBUG)", }),
(("-q",      "--quiet",         ),{ "dest": "verbosity",         "action": "store_const", "const": -1, "help": "Do not output anything", }),
(("-a",      "--allow-unknown", ),{ "dest": "allow_unknown",     "action": "store_true",         "help": "hyphenate even unknown words (Use with care!)", }),
(("-l",      "--list-unknown",  ),{ "dest": "list_unknown",      "action": "store_true",         "help": "list unknown words and their guessed hyphenations (Dry run implied)", }),
(("-k", "--known-hyphenations", ),{ "dest": "hyphenations_file", "metavar": "HYPHENATIONS.yaml", "help": "read known hyphenations from this file (YAML format)", }),
(("--known", "--hyphenations",  ),{ "dest": "hyphenations_file",                                 "help": argparse.SUPPRESS, }),
(("-O",      "--output-path",   ),{ "dest": "output_path",       "metavar": "PATH",              "help": "output directory for hyphenated HTML documents", }),
(("--out",   "--output",        ),{ "dest": "output_path",                                       "help": argparse.SUPPRESS, }),
(("--output-name",              ),{ "dest": "output_name",       "metavar": "PATTERN",           "help": "name for output files (Default: \"{name}_hyphenated.{ext}\")", }),
(("--output-format",            ),{ "dest": "output_format",     "metavar": "FORMAT",            "help": f"format for output files ({ ', '.join(list(FORMATS.keys())) }) (Default: html)", }),
(("--format", "--fmt"           ),{ "dest": "output_format",                                     "help": argparse.SUPPRESS, }),
(("-o",      "--overwrite",     ),{ "dest": "overwrite",         "action": "store_true",         "help": "overwrite already existing files", }),
(("--config",                   ),{ "dest": "config_file",       "metavar": "CONFIG.yaml",       "help": "read configuration from this file (YAML format)", }),
(("--log-level",                ),{ "dest": "log_level",         "metavar": "LEVEL", "choices": VERBOSITY.keys(), "help": f"set logging level ({ ', '.join(list(VERBOSITY.keys())) }) (Default: {APP_CFG['log_level']})", }),
(("--loglevel",                 ),{ "dest": "log_level",         "choices": VERBOSITY.keys(),    "help": argparse.SUPPRESS, }),
(("--dry-run",                  ),{ "dest": "dry_run",           "action": "store_true",         "help": "do not do anything", }),
(("--dryrun",                   ),{ "dest": "dry_run",           "action": "store_true",         "help": argparse.SUPPRESS, }),
)

# -----------------------------------------------------------------------------

def cli():
    set_up_and_run_application(APP_NAME, APP_DESCRIPTION, APP_USAGE, APP_CLI_ARGUMENTS, APP_CFG, main)

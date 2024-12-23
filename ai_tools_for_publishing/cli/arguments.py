import argparse
from typing import Dict, Tuple, Any


def parse_arguments(
    APP_NAME: str,
    APP_DESCRIPTION: str,
    APP_USAGE: str,
    APP_CLI_ARGUMENTS: Tuple[Tuple],
) -> Dict[str, Any]:
    """Parse command-line arguments.

    :param APP_NAME:          The name of the application.
    :param APP_DESCRIPTION:   A brief description of the application.
    :param APP_USAGE:         Usage information for the application.
    :param APP_CLI_ARGUMENTS: List of command-line arguments to parse.

    :return: A dictionary with the parsed arguments.
    """
    argparser = argparse.ArgumentParser(
        prog=APP_NAME,
        description=APP_DESCRIPTION,
        epilog=APP_USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Add arguments to the parser and parse them
    for arg in APP_CLI_ARGUMENTS:
        argparser.add_argument(*arg[0], **arg[1])
    args_cfg = vars(argparser.parse_args())

    # Remove empty arguments so that they don't override the .config file
    args_cfg = {name: value for name, value in args_cfg.items() if value}

    return args_cfg

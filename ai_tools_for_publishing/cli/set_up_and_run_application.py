import sys
import logging
from typing import Callable, Dict, Tuple, Any
from .arguments import parse_arguments
from .config import set_up_config
from .logging import set_up_loggers, VERBOSITY


def set_up_and_run_application(
    APP_NAME: str,
    APP_DESCRIPTION: str,
    APP_USAGE: str,
    APP_CLI_ARGUMENTS: Tuple[Tuple],
    APP_CFG: Dict[str, Any],
    main: Callable,
) -> None:
    """Parse command line arguments, set up logging and configuration,
    and run the application.

    :param APP_NAME:          The name of the application.
    :param APP_DESCRIPTION:   A brief description of the application.
    :param APP_USAGE:         Usage information for the application.
    :param APP_CLI_ARGUMENTS: List of command-line arguments to parse.
    :param APP_CFG:           Default configuration for the application.
    :param main:              The main function of the application

    This function never returns. It exits the program with return code.
    """

    # Start a screen logger that can handle error messages
    set_up_loggers()
    log = logging.getLogger(__name__)

    try:
        # Here we go!
        log.info("Starting %s...", APP_NAME)

        # Parse command-line arguments
        args_cfg = parse_arguments(
            APP_NAME, APP_DESCRIPTION, APP_USAGE, APP_CLI_ARGUMENTS
        )

        # Make sure that verbosity is within range and convert it into a string
        if "verbosity" in args_cfg:
            verbosity_names = tuple(VERBOSITY.keys())
            args_cfg["verbosity"] = verbosity_names[
                (
                    len(verbosity_names) - 1
                    if args_cfg["verbosity"] + 2 > len(verbosity_names)
                    else args_cfg["verbosity"] + 1
                )
            ]

        # Combine defaults and arguments, possibly read a configuration file
        cfg = set_up_config(APP_CFG, args_cfg)

        # Update logging levels according to the configuration
        set_up_loggers(cfg)

        # Log the command line arguments and the configuration
        log.debug("Command line arguments", extra={"raw": sys.argv, "parsed": args_cfg})
        log.debug("Configuration", extra={"cfg": cfg})

        # Run the application
        main(cfg)

    except Exception as error:
        log.exception(error.__class__.__name__, extra={"problem": str(error)})

        # Raise the exception to the terminal when debugging
        if args_cfg.get("verbosity") == "DEBUG":
            raise
        sys.exit(1)

    log.info("All Ok!")
    sys.exit(0)

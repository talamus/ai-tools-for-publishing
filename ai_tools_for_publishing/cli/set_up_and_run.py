import sys
import logging
from typing import Callable, Dict, Any
from .config import set_up_config
from .logging import set_up_loggers, VERBOSITY


def set_up_and_run(
    program_name: str,
    program: Callable,
    default_cfg: Dict[str, Any],
    args_cfg: Dict[str, Any],
) -> int:
    """Set up logging and configuration. Run the program.

    :param program_name: Name of the program.
    :param program: The main function of the program.
        It is expected to take a configuration dictionary as an argument
        and throw exceptions if something goes wrong.

    :param default_cfg: Default configuration for the program.
    :param args_cfg: Configuration from command line options.

    :return: 0 if everything went well, 1 if there was an error.
    """

    # Start a screen logger that can handle error messages
    set_up_loggers()
    log = logging.getLogger(__name__)

    try:
        # Here we go!
        log.info("Starting %s...", program_name)

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
        cfg = set_up_config(default_cfg, args_cfg)

        # Update logging levels according to the configuration
        set_up_loggers(cfg)

        # Log the command line arguments and the configuration
        log.debug("Command line arguments", extra={"raw": sys.argv, "parsed": args_cfg})
        log.debug("Configuration", extra={"cfg": cfg})

        # Run the application
        program(cfg)

    except Exception as error:
        log.exception(error.__class__.__name__, extra={"problem": str(error)})

        # Raise the exception to the terminal when debugging
        if args_cfg.get("verbosity") == "DEBUG":
            raise
        return 1

    log.info("All Ok!")
    return 0

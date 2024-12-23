import os.path
from typing import Any
from ai_tools_for_publishing.utils import read_yaml_file_to_dict


def set_up_config(
    defaults: dict[str, Any], overrides: dict[str, Any]
) -> dict[str, Any]:
    """
    Build configuration for the application.
    """

    if "config_file" in overrides:
        config = read_yaml_file_to_dict(overrides["config_file"])
    elif "config_file" in defaults and os.path.exists(defaults["config_file"]):
        config = read_yaml_file_to_dict(defaults["config_file"])
    else:
        config = {}

    config = defaults | config
    config = config | overrides
    return config

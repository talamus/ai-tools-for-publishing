import yaml
from typing import Any, Dict
import re


class MultilineDumper(yaml.SafeDumper):
    """A custom YAML dumper that handles multiline strings correctly."""

    def represent_str(self, data):
        """Represent multiline strings in pipe style and other strings with double quotes, unless they contain special characters."""
        if "\n" in data:
            return self.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        if re.search(r"[^\w]", data):
            return self.represent_scalar("tag:yaml.org,2002:str", data, style='"')
        return self.represent_scalar("tag:yaml.org,2002:str", data)


# Register the string representer to our dumper
MultilineDumper.add_representer(str, MultilineDumper.represent_str)


def dict_to_yaml_str(data: Dict[str, Any]) -> str:
    """
    Dump a dictionary to a YAML string.
    Handle multiline strings correctly.
    """
    return yaml.dump(
        data,
        Dumper=MultilineDumper,
        allow_unicode=True,
        sort_keys=True,
        default_flow_style=False,
    )


def read_yaml_file_to_dict(file_name: str) -> Dict[str, Any]:
    """
    Read a YAML file and return a dictionary.
    Throw an error if something goes wrong.
    """
    with open(file_name) as stream:
        content = yaml.safe_load(stream)
    if not isinstance(content, dict):
        raise TypeError(f"'{file_name}' is not a YAML dictionary")
    return content

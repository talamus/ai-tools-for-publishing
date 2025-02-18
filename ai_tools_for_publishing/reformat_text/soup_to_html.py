from typing import Dict, Any
from bs4 import BeautifulSoup
from bs4.formatter import Formatter, EntitySubstitution


def soup_to_html(
    soup: BeautifulSoup, templating_variables: Dict[str, str], cfg: Dict[str, Any]
) -> str:
    """Convert a BeautifulSoup object to an HTML string."""

    html5_formatter = Formatter(
        entity_substitution=EntitySubstitution.substitute_xml,
        void_element_close_prefix=None,
    )
    return soup.decode(formatter=html5_formatter)

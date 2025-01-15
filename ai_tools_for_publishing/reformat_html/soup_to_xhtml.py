import logging
from typing import Any, Dict
from bs4 import BeautifulSoup
from bs4.formatter import Formatter, EntitySubstitution


def soup_to_xhtml(
    soup: BeautifulSoup, templating_variables: Dict[str, str], cfg: Dict[str, Any]
) -> str:
    """Convert a BeautifulSoup object to an XHTML string."""

    log = logging.getLogger(__name__)

    body = soup.find("body")
    if not body:
        raise SyntaxError("No <body> tag found")

    xhtml_formatter = Formatter(entity_substitution=EntitySubstitution.substitute_xml)

    content = body.decode(formatter=xhtml_formatter)

    author_tag = soup.find("meta", attrs={"name": "author"})
    copyright_tag = soup.find("meta", attrs={"name": "copyright"})
    vars_from_html = {
        "language": soup.find("html")
        .get("lang", body.get("lang", "en"))
        .strip()
        .lower(),
        "title": soup.find("title").get_text().strip() if soup.find("title") else "",
        "author": author_tag.get("content", "").strip() if author_tag else "",
        "copyright": copyright_tag.get("content").strip() if copyright_tag else "",
        "content": content,
    }
    combined_vars = vars_from_html | templating_variables
    log.debug("Combined templating variables", extra={"combined_vars": combined_vars})

    return cfg["xhtml_template"].format(**combined_vars)

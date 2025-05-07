import logging
from typing import Any, Dict
from bs4 import BeautifulSoup
from bs4.formatter import Formatter, EntitySubstitution
from .get_body_from_soup import get_body_from_soup


def soup_to_xhtml(
    soup: BeautifulSoup, templating_variables: Dict[str, str], cfg: Dict[str, Any]
) -> str:
    """Convert a BeautifulSoup object to an XHTML string."""

    log = logging.getLogger(__name__)
    body = get_body_from_soup(soup)

    xhtml_formatter = Formatter(entity_substitution=EntitySubstitution.substitute_xml)
    content = body.decode(formatter=xhtml_formatter)
    log.debug("Content", extra={"content": content})

    html_tag = soup.find("html")
    body_tag = soup.find("body")
    title_tag = soup.find("title")
    author_tag = soup.find("meta", attrs={"name": "author"})
    copyright_tag = soup.find("meta", attrs={"name": "copyright"})

    language = (
        html_tag.get("lang") if html_tag else body_tag.get("lang") if body_tag else "en"
    )
    language = language.strip().lower()

    vars_from_html = {
        "language": language,
        "title": title_tag.get_text().strip() if title_tag else "",
        "author": author_tag.get("content", "").strip() if author_tag else "",
        "copyright": copyright_tag.get("content").strip() if copyright_tag else "",
        "content": content,
    }
    combined_vars = vars_from_html | templating_variables
    log.debug("Combined templating variables", extra={"combined_vars": combined_vars})

    return cfg["xhtml_template"].format(**combined_vars)

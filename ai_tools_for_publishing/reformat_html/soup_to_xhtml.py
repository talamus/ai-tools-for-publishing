from bs4 import BeautifulSoup
from lxml import html, etree
from typing import Any, Dict


def soup_to_xhtml(
    soup: BeautifulSoup, templating_variables: Dict[str, str], cfg: Dict[str, Any]
) -> str:
    """Convert a BeautifulSoup object to an XHTML string."""

    body = soup.find("body")
    if not body:
        raise SyntaxError("No <body> tag found")

    parser = html.HTMLParser()
    tree = html.fromstring(str(body), parser=parser)

    content = (
        etree.tostring(tree, pretty_print=True, method="xml", encoding="UTF-8")
        .decode("UTF-8")
        .strip()
    )

    author_tag = soup.find("meta", attrs={"name": "author"})
    copyright_tag = soup.find("meta", attrs={"name": "copyright"})
    vars = {
        "language": soup.find("html").get(
            "lang", templating_variables.get("language", "en")
        ),
        "title": (
            soup.find("title").get_text()
            if soup.find("title")
            else templating_variables.get("title", "")
        ),
        "author": (
            author_tag.get("content", "")
            if author_tag
            else templating_variables.get("author", "")
        ),
        "copyright": (
            copyright_tag.get("content", "")
            if copyright_tag
            else templating_variables.get("copyright", "")
        ),
        "content": content,
    }

    return cfg["xhtml_template"].format(**vars)

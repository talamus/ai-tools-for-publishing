import re
import logging
from typing import Any, Dict
from bs4 import BeautifulSoup, Tag, NavigableString
from .get_body_from_soup import get_body_from_soup

# fmt: off
ALLOWED_TAGS = {
    "h1": {     "format": "<h1>{content}</h1>\n", "allowed_tags": ("br", "em", "i", "strong", "b", ) },
    "h2": {     "format": "<h2>{content}</h2>\n", "allowed_tags": ("br", "em", "i", "strong", "b", ) },
    "h3": {     "format": "<h3>{content}</h3>\n", "allowed_tags": ("br", "em", "i", "strong", "b", ) },
    "h4": {     "format": "<h4>{content}</h4>\n", "allowed_tags": ("br", "em", "i", "strong", "b", ) },
    "h5": {     "format": "<h5>{content}</h5>\n", "allowed_tags": ("br", "em", "i", "strong", "b", ) },
    "p":  {     "format": "<p>{content}</p>\n", "allowed_tags": ("br", "em", "i", "strong", "b", ) },
    "hr": {     "format": "<hr>", "allowed_tags": tuple() },
    "br": {     "format": "<br>\n", "allowed_tags": tuple() },
    "em": {     "format": "<em>{content}</em>", "allowed_tags": tuple() },
    "i":  {     "format": "<i>{content}</i>", "allowed_tags": tuple() },
    "strong": { "format": "<strong>{content}</strong>", "allowed_tags": tuple() },
    "b": {      "format": "<b>{content}</b>", "allowed_tags": tuple() },
    "blockquote": { "format": "<blockquote>\n{content}\n</blockquote>\n", "allowed_tags": ("p", ) },
}
# fmt: on


MULTIPLE_WHITESPACE = re.compile(r"\s+")


def tags_to_str(parent: Tag, allowed_tags: tuple[str]) -> str:
    """Iterate over children and convert recursively to string."""
    parent_content = ""
    for tag in parent:

        if isinstance(tag, NavigableString):
            parent_content += MULTIPLE_WHITESPACE.sub(" ", str(tag))
            continue

        if tag.name in allowed_tags:
            format = ALLOWED_TAGS[tag.name]["format"]
            content = tags_to_str(tag, ALLOWED_TAGS[tag.name]["allowed_tags"])
        else:
            format = "{content}"
            content = tags_to_str(tag, allowed_tags)

        parent_content += format.format(content=content)

    return parent_content


def soup_to_simplified_html(
    soup: BeautifulSoup, templating_variables: Dict[str, str], cfg: Dict[str, Any]
) -> str:
    """Convert a BeautifulSoup object to a simplified HTML string."""

    log = logging.getLogger(__name__)
    body = get_body_from_soup(soup)

    content = tags_to_str(body, tuple(ALLOWED_TAGS.keys())).strip()
    content = re.sub(r" *\n *", "\n", content)
    content = re.sub(r"\n+", "\n", content)
    content = re.sub(r"<p> +</p>", "<p></p>", content)
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

    return cfg["simplified_html_template"].format(**combined_vars)

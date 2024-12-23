import logging
import textwrap
from typing import Any, Dict
from bs4 import BeautifulSoup, Tag, NavigableString
from ai_tools_for_publishing.utils import simplify_punctuation
from .default_config import DEFAULT_CONFIG


def convert_tag_to_markdown(tags: Tag) -> str:
    content = ""
    for tag in tags:

        # Strings
        if isinstance(tag, NavigableString):
            if str(tag) != "\n":
                content += str(tag)
            continue

        # Tags
        if tag.name not in ALLOWED_TAGS:
            raise SyntaxError(f"Unsupported tag {tag.name}: {str(tag)}")
        content += ALLOWED_TAGS[tag.name](tag)

    return content


ALLOWED_TAGS = {
    "h1": lambda soup: "# " + convert_tag_to_markdown(soup) + "\n\n",
    "h2": lambda soup: "## " + convert_tag_to_markdown(soup) + "\n\n",
    "h3": lambda soup: "### " + convert_tag_to_markdown(soup) + "\n\n",
    "h4": lambda soup: "#### " + convert_tag_to_markdown(soup) + "\n\n",
    "h5": lambda soup: "##### " + convert_tag_to_markdown(soup) + "\n\n",
    "p": lambda soup: convert_tag_to_markdown(soup) + "\n\n",
    "hr": lambda soup: "---\n\n",
    "br": lambda soup: " ",
    "em": lambda soup: "'" + convert_tag_to_markdown(soup) + "'",
    "i": lambda soup: convert_tag_to_markdown(soup),
    "strong": lambda soup: "*" + convert_tag_to_markdown(soup) + "*",
    "b": lambda soup: convert_tag_to_markdown(soup),
    "blockquote": lambda soup: textwrap.indent(convert_tag_to_markdown(soup), "    "),
}


def soup_to_markdown(
    soup: BeautifulSoup, templating_variables: Dict[str, str], cfg: Dict[str, Any]
) -> str:
    """Convert a BeautifulSoup object to a simplified Markdown string."""

    body = soup.find("body")
    if not body:
        raise SyntaxError("No <body> tag found")

    content = convert_tag_to_markdown(body)
    content = simplify_punctuation(content)
    return content

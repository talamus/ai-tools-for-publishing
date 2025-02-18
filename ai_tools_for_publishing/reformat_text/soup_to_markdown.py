import re
import textwrap
from typing import Any, Dict
from bs4 import BeautifulSoup, Tag, NavigableString
from ai_tools_for_publishing.utils import simplify_punctuation
from .default_config import DEFAULT_CONFIG
from .get_body_from_soup import get_body_from_soup

def convert_tag_to_markdown(tags: Tag) -> str:
    """
    Take a BeautifulSoup tag and return a simplified Markdown string.
    This function is recursive, so it can handle nested tags.
    """
    content = ""
    for tag in tags:

        # Strings
        if isinstance(tag, NavigableString):
            # Replace all continuations of whitespaces with a single space
            str_tag = re.sub(r"\s+", " ", str(tag))
            if str_tag != " ":
                content += str_tag

            # Remove the extra space that happens with <br> tags
            content = re.sub("\b ?", "", content)
            continue

        # Tags
        if tag.name not in ALLOWED_TAGS:
            raise SyntaxError(f"Unsupported tag {tag.name}: {str(tag)}")
        content += ALLOWED_TAGS[tag.name](tag)

    return content


def each_sentence_on_new_line(content: str) -> str:
    """
    Add a newline after each sentence.
    Paragraphs will still follow the markdown syntax, but diffs will be easier to read.
    """
    lines = content.split("\n")
    new_content = []
    for line in lines:
        if line == "" or line.startswith(" ") or line.startswith("#"):
            new_content.append(line)
        else:
            new_content.append(re.sub(r"([.!?])\s+", r"\1\n", line))
    return "\n".join(new_content)


ALLOWED_TAGS = {
    "h1": lambda soup: "# " + convert_tag_to_markdown(soup) + "\n\n",
    "h2": lambda soup: "## " + convert_tag_to_markdown(soup) + "\n\n",
    "h3": lambda soup: "### " + convert_tag_to_markdown(soup) + "\n\n",
    "h4": lambda soup: "#### " + convert_tag_to_markdown(soup) + "\n\n",
    "h5": lambda soup: "##### " + convert_tag_to_markdown(soup) + "\n\n",
    "p": lambda soup: convert_tag_to_markdown(soup) + "\n\n",
    "hr": lambda soup: "---\n\n",
    "br": lambda soup: "\n\b",  # See: convert_tag_to_markdown()
    "em": lambda soup: "'" + convert_tag_to_markdown(soup) + "'",
    "strong": lambda soup: "*" + convert_tag_to_markdown(soup) + "*",
    "i": lambda soup: convert_tag_to_markdown(soup),  # These two are designed to
    "b": lambda soup: convert_tag_to_markdown(soup),  # be ignored
    "blockquote": lambda soup: textwrap.indent(convert_tag_to_markdown(soup), "    "),
}


def soup_to_markdown(
    soup: BeautifulSoup, templating_variables: Dict[str, str], cfg: Dict[str, Any]
) -> str:
    """Convert a BeautifulSoup object to a simplified Markdown string."""
    body = get_body_from_soup(soup)
    content = convert_tag_to_markdown(body)
    content = simplify_punctuation(content)
    return content

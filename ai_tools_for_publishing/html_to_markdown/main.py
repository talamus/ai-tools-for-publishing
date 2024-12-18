import os.path
import logging
import textwrap
from bs4 import BeautifulSoup, Tag, NavigableString
from .default_config import DEFAULT_CONFIG

ALLOWED_TAGS = {
    "h1": lambda soup: "# " + convert_soup_to_markdown(soup) + "\n\n",
    "h2": lambda soup: "## " + convert_soup_to_markdown(soup) + "\n\n",
    "h3": lambda soup: "### " + convert_soup_to_markdown(soup) + "\n\n",
    "h4": lambda soup: "#### " + convert_soup_to_markdown(soup) + "\n\n",
    "h5": lambda soup: "##### " + convert_soup_to_markdown(soup) + "\n\n",
    "p": lambda soup: convert_soup_to_markdown(soup) + "\n\n",
    "hr": lambda soup: "---\n\n",
    "br": lambda soup: "\n",
    "em": lambda soup: "'" + convert_soup_to_markdown(soup) + "'",
    "i": lambda soup: "'" + convert_soup_to_markdown(soup) + "'",
    "strong": lambda soup: "*" + convert_soup_to_markdown(soup) + "*",
    "b": lambda soup: "*" + convert_soup_to_markdown(soup) + "*",
    "blockquote": lambda soup: textwrap.indent(convert_soup_to_markdown(soup), "   "),
}

CHARACTER_REPLACEMENTS = {
    "\N{LEFT SINGLE QUOTATION MARK}": "'",
    "\N{RIGHT SINGLE QUOTATION MARK}": "'",
    "\N{LEFT DOUBLE QUOTATION MARK}": '"',
    "\N{RIGHT DOUBLE QUOTATION MARK}": '"',
    "\N{HORIZONTAL ELLIPSIS}": "...",
    "\N{NON-BREAKING HYPHEN}": "-",
    "\N{MINUS SIGN}": "-",
    "\N{EM DASH}": "\N{EN DASH}",
    "\N{NO-BREAK SPACE}": " ",
}


def convert_soup_to_markdown(soup: Tag) -> str:
    """Convert HTML tags to Markdown."""
    global ALLOWED_TAGS

    content = ""
    for tag in soup:

        # Strings
        if isinstance(tag, NavigableString):
            if str(tag) != "\n":
                content = content + str(tag)
            continue

        # Tags
        if tag.name not in ALLOWED_TAGS:
            raise SyntaxError(f"Illegal tag {tag.name}: {str(tag)}")
        content = content + ALLOWED_TAGS[tag.name](tag)

    return content


def simplify_punctuation(content: str) -> str:
    """Simplify the typographic punctuation."""
    global CHARACTER_REPLACEMENTS
    for original, replacement in CHARACTER_REPLACEMENTS.items():
        content = content.replace(original, replacement)
    return content


def html_to_markdown(in_file: str, out_file: str | None, cfg: dict = None) -> None:
    """Convert a HTML document to a very plain Markdown file."""
    if cfg is None:
        cfg = dict(DEFAULT_CONFIG)
    log = logging.getLogger(__name__)

    if not out_file:
        out_file = os.path.splitext(in_file)[0] + ".md"

    if os.path.exists(out_file) and not cfg["overwrite"]:
        raise FileExistsError(out_file)

    log.info("Reading HTML file", extra={"file": in_file})
    html = open(in_file).read()

    log.info("Parsing it")
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("body")
    if body is not None:
        soup = body
    log.debug("Beautiful Soup", extra={"html": soup})

    log.info("Converting to Markdown")
    md = convert_soup_to_markdown(soup)
    log.debug("Markdown", extra={"md": md})

    log.info("Simplifing punctiation")
    md = simplify_punctuation(md)
    log.debug("Simplified", extra={"md": md})

    if not cfg["dryrun"]:
        log.info("Writing Markdown file", extra={"file": out_file})
        open(out_file, "w").write(md)

from typing import Any, Dict
from .soup_to_html import soup_to_html
from .soup_to_xhtml import soup_to_xhtml
from .soup_to_markdown import soup_to_markdown, each_sentence_on_new_line
from .soup_to_simplified_html import soup_to_simplified_html


FORMATS = {
    "html": {
        "description": "Parsed HTML file",
        "extension": "_parsed.html",
        "formatter": soup_to_html,
    },
    "simplified_html": {
        "description": "Simplified HTML file",
        "extension": "_simplified.html",
        "formatter": soup_to_simplified_html,
    },
    "xhtml": {
        "description": "XHTML file suitable for EPUB",
        "extension": "_reformatted.xhtml",
        "formatter": soup_to_xhtml,
    },
    "md": {
        "description": "Simplified Markdown file",
        "extension": "_reformatted.md",
        "formatter": soup_to_markdown,
    },
    "paragraph_md": {
        "description": "Paragraph separated Markdown file",
        "extension": ".md",
        "formatter": lambda soup, templating_variables, cfg: each_sentence_on_new_line(
            soup_to_markdown(soup, templating_variables, cfg)
        ),
    },
}


def match_str_to_format(partial_format_str: str) -> Dict[str, Any]:
    """Find the format that matches the partial format name."""
    for key in FORMATS.keys():
        if key.startswith(partial_format_str[0].lower()):
            return FORMATS[key]
    raise ValueError(f"Unknown format: {partial_format_str}")

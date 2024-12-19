from bs4 import BeautifulSoup
from lxml import html, etree


def write_xhtml_file(output_file: str, soup: BeautifulSoup, cfg: dict) -> None:

    body = soup.find("body")
    if not body:
        raise SyntaxError("No <body> tag")

    parser = html.HTMLParser()
    tree = html.fromstring(str(body), parser=parser)

    content = (
        etree.tostring(tree, pretty_print=True, method="xml", encoding="UTF-8")
        .decode("UTF-8")
        .strip()
    )

    author_tag = soup.find("meta", attrs={"name": "author"})
    copyright_tag = soup.find("meta", attrs={"name": "copyright"})
    fields = {
        "language": soup.find("html").get("lang", "en"),
        "title": soup.find("title").get_text() if soup.find("title") else "",
        "author": author_tag.get("content", "") if author_tag else "",
        "copyright": copyright_tag.get("content", "") if copyright_tag else "",
        "content": content,
    }

    with open(output_file, "w") as file:
        file.write(cfg["xhtml_template"].format(**fields))

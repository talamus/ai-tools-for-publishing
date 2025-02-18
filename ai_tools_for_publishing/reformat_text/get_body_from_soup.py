import logging
from bs4 import BeautifulSoup, Tag

def get_body_from_soup(soup: BeautifulSoup) -> Tag:
    """
    Return the <body> tag from a BeautifulSoup object,
    or the entire soup if no <body> tag is found.
    """
    log = logging.getLogger(__name__)
    body = soup.find("body")
    if not body:
        log.info("<body> not found, using soup")
        return soup
    else:
        return body

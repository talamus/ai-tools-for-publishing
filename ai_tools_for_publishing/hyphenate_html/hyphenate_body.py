import re
import logging
from typing import Dict, Any
from bs4 import Tag
from libvoikko import Voikko
from ai_tools_for_publishing.punctuation import (
    ALL_PUNCTUATION,
    split_punctuation_from_word,
)

try:
    VOIKKO = Voikko("fi")
except Exception:
    raise Exception(
        """Unable to launch Finnish language Voikko

Please make sure that the libvoikko and the
Finnish language dictionary have been installed:

    sudo apt install libvoikko1 voikko-fi\n"""
    )


def hyphenate_word(word: str, known_hyphenations: Dict[str, str]) -> str:
    """Hyphenate a single word and return it."""
    global VOIKKO
    log = logging.getLogger(__name__)

    prefix, word, postfix = split_punctuation_from_word(word)
    if word in known_hyphenations:
        log.debug("Known word %s -> %s", word, known_hyphenations[word])
        hyphenated_word = known_hyphenations[word].replace("_", "\N{SOFT HYPHEN}")
    else:
        hyphenated_word = VOIKKO.hyphenate(word, separator="\N{SOFT HYPHEN}")
        if not isinstance(hyphenated_word, str):
            raise TypeError(f"Hyphenating '{word}' returned {hyphenated_word}")

        # Voikko adds hyphenation after punctuation in multi-part words,
        # let's remove it...
        fixed_hyphenated_word = re.sub(
            f"([{re.escape(ALL_PUNCTUATION)}])\N{SOFT HYPHEN}",
            lambda m: m[1],
            hyphenated_word,
        )

        if hyphenated_word != fixed_hyphenated_word:
            log.warning(
                "Voikko hyphenation fixed",
                extra={
                    "original": hyphenated_word.replace("\N{SOFT HYPHEN}", "_"),
                    "fixed": fixed_hyphenated_word.replace("\N{SOFT HYPHEN}", "_"),
                },
            )
            hyphenated_word = fixed_hyphenated_word

    return prefix + hyphenated_word + postfix


def hyphenate_paragraph(sentence: str, known_hyphenations: Dict[str, str]) -> str:
    """Hyphenate a single paragraph and return it."""

    # We are preserving the original whitespace in the sentence:
    old_words = re.split(r"(\s+)", sentence)
    new_words = []
    for word in old_words:
        if word == "" or word.isspace():
            new_words.append(word)
        else:
            new_words.append(hyphenate_word(word, known_hyphenations))
    return "".join(new_words)


def hyphenate_body(
    body: Tag, known_hyphenations: Dict[str, str], cfg: Dict[str, Any]
) -> None:
    """Hyphenate the text in-place in the <body> tag."""

    global VOIKKO
    VOIKKO.setNoUglyHyphenation(True)
    VOIKKO.setHyphenateUnknownWords(cfg["allow_unknown"])
    VOIKKO.setMinHyphenatedWordLength(cfg["min_word_length"])

    for element in body.find_all(string=True):
        if element == "\n":
            continue
        sentence = str(element).replace("\N{SOFT HYPHEN}", "")
        element.replace_with(hyphenate_paragraph(sentence, known_hyphenations))

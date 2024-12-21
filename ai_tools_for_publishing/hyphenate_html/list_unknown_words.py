import re
import logging
import yaml
from bs4 import Tag
from libvoikko import Voikko
from ai_tools_for_publishing.punctuation import (
    ALL_PUNCTUATION,
    split_punctuation_from_word,
)

try:
    VOIKKO = Voikko("fi")
    VOIKKO.setNoUglyHyphenation(True)
    VOIKKO.setHyphenateUnknownWords(True)
    VOIKKO.setMinHyphenatedWordLength(1)
    STRICT_VOIKKO = Voikko("fi")
    STRICT_VOIKKO.setNoUglyHyphenation(False)
    STRICT_VOIKKO.setHyphenateUnknownWords(False)
    STRICT_VOIKKO.setMinHyphenatedWordLength(1)
except Exception:
    raise Exception(
        """Unable to launch Finnish language Voikko

Please make sure that the libvoikko and the
Finnish language dictionary have been installed:

    sudo apt install libvoikko1 voikko-fi\n"""
    )


unknown_words = dict()


def collect_unknown_words(file: str, body: Tag, cfg: dict) -> None:
    global unknown_words
    global VOIKKO
    global STRICT_VOIKKO

    VOIKKO.setMinHyphenatedWordLength(cfg["min_word_length"])

    log = logging.getLogger(__name__)
    log.info("Listing %s", file)

    for element in body.find_all(string=True):
        if element == "\n":
            continue

        words = str(element).split()
        for word in words:
            word = split_punctuation_from_word(word)[1]

            if len(word) < 5:
                continue

            pattern = STRICT_VOIKKO.getHyphenationPattern(word).split()
            if not pattern and word not in unknown_words:
                hyphenated_word = VOIKKO.hyphenate(word, separator="_")

                # Voikko adds hyphenation after punctuation in multi-part words,
                # let's remove it...
                hyphenated_word = re.sub(
                    f"([{re.escape(ALL_PUNCTUATION)}])_",
                    lambda m: m[1],
                    hyphenated_word,
                )

                unknown_words[word] = hyphenated_word


def print_unknown_words():
    global unknown_words
    print(yaml.dump(unknown_words, allow_unicode=True, default_flow_style=False))

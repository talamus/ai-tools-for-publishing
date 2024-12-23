import re
import yaml
from typing import Dict, Any
from bs4 import Tag
from .voikko import get_voikko, get_strict_voikko
from ai_tools_for_publishing.utils import ALL_PUNCTUATION, split_punctuation_from_word

# Dictionary of unknown words and their (guessed) hyphenated forms
unknown_words: Dict[str, str] = dict()


def collect_unknown_words(body: Tag) -> None:
    """Detect words that Voikko does not recognize
    and add them to the dictionary of unknown words.
    """
    global unknown_words

    voikko = get_voikko()
    strict_voikko = get_strict_voikko()

    for element in body.find_all(string=True):
        if element == "\n":
            continue

        words = str(element).split()
        for word in words:
            word = split_punctuation_from_word(word)[1]

            if len(word) < 5:
                continue

            pattern = strict_voikko.getHyphenationPattern(word).split()
            if not pattern and word not in unknown_words:
                hyphenated_word = voikko.hyphenate(word, separator="_")

                # Voikko adds hyphenation after punctuation in multi-part words,
                # let's remove it...
                hyphenated_word = re.sub(
                    f"([{re.escape(ALL_PUNCTUATION)}])_",
                    lambda m: m[1],
                    hyphenated_word,
                )

                unknown_words[word] = hyphenated_word


def print_unknown_words() -> None:
    """Print the dictionary of unknown words
    and their hyphenated forms in YAML format."""
    global unknown_words
    print(
        yaml.dump(unknown_words, allow_unicode=True, default_flow_style=False), end=""
    )

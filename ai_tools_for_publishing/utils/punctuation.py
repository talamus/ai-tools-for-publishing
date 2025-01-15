import re
import logging

RAW = 0
PRETTY = 1
SIMPLIFIED = 2

# fmt: off
CANONIZED_PUNCTUATION = ( #                 Pretty version                              Simplified version
("\N{HORIZONTAL ELLIPSIS}",                 "\N{HORIZONTAL ELLIPSIS}",                  "..."),
("...",                                     "\N{HORIZONTAL ELLIPSIS}",                  "..."),

("\N{LEFT DOUBLE QUOTATION MARK}",          "\N{RIGHT DOUBLE QUOTATION MARK}",          '"'),
("\N{RIGHT DOUBLE QUOTATION MARK}",         "\N{RIGHT DOUBLE QUOTATION MARK}",          '"'),
('"',                                       "\N{RIGHT DOUBLE QUOTATION MARK}",          '"'),

("\N{LEFT SINGLE QUOTATION MARK}",          "\N{RIGHT SINGLE QUOTATION MARK}",          "'"),
("\N{RIGHT SINGLE QUOTATION MARK}",         "\N{RIGHT SINGLE QUOTATION MARK}",          "'"),
("'",                                       "\N{RIGHT SINGLE QUOTATION MARK}",          "'"),

("\N{EM DASH}",                             "\N{EN DASH}",                              "\N{EN DASH}"),
("\N{EN DASH}",                             "\N{EN DASH}",                              "\N{EN DASH}"),
("\N{NON-BREAKING HYPHEN}",                 "\N{NON-BREAKING HYPHEN}",                  "-"),
("\N{MINUS SIGN}",                          "\N{MINUS SIGN}",                           "-"),

("\N{NO-BREAK SPACE}",                      "\N{NO-BREAK SPACE}",                       " "),
)
# fmt: on

ALL_PUNCTUATION = "!?:;.,()*+-/[]_" + "".join(
    [p[RAW] for p in CANONIZED_PUNCTUATION if p[RAW][0] not in "!?:;.,()*+-/[]_"]
)

PRETTIFY_PUNCTUATION = dict()
SIMPLIFY_PUNCTUATION = dict()
for p in CANONIZED_PUNCTUATION:
    PRETTIFY_PUNCTUATION[p[RAW]] = p[PRETTY]
    SIMPLIFY_PUNCTUATION[p[RAW]] = p[SIMPLIFIED]

SPLIT_PUNCTUATION_RE = re.compile(
    f"^([{re.escape(ALL_PUNCTUATION)}]*)(.*?)([{re.escape(ALL_PUNCTUATION)}]*)$"
)


def split_punctuation_from_word(word: str) -> str:
    """
    Returns three pieces: (prefix, word, postfix)
    The word is always in the middle piece.
    """
    global SPLIT_PUNCTUATION_RE
    log_unknown_punctuation(word)
    parts = SPLIT_PUNCTUATION_RE.search(word)
    if parts == None:
        raise Exception(f"Unable to split word '{word}'")
    return (parts[1], parts[2], parts[3])


def strip_punctuation(word: str) -> str:
    """
    Removes punctuation around the word.
    Keeps pre and post dashes that are important in Finnish language.
    """
    word = word.strip()
    starts_with_dash = word.startswith("-")
    ends_with_dash = word.endswith("-")
    word = split_punctuation_from_word(word)[1]
    if starts_with_dash:
        word = "-" + word
    if ends_with_dash:
        word = word + "-"
    return word


def prettify_punctuation(word: str) -> str:
    """
    Unify punctuation to be press ready.
    """
    log_unknown_punctuation(word)
    global PRETTIFY_PUNCTUATION
    for raw, pretty in PRETTIFY_PUNCTUATION.items():
        word = word.replace(raw, pretty)
    return word


def simplify_punctuation(word: str) -> str:
    """
    Unify punctuation to be AI ready.
    """
    log_unknown_punctuation(word)
    global SIMPLIFY_PUNCTUATION
    for raw, simple in SIMPLIFY_PUNCTUATION.items():
        word = word.replace(raw, simple)
    return word


already_logged_punctuation = dict()


def log_unknown_punctuation(word: str) -> None:
    """
    Check for unknown punctuation characters and log a warning.
    """
    global ALL_PUNCTUATION
    global already_logged_punctuation
    log = logging.getLogger(__name__)
    for char in word:
        if (
            not char.isspace()
            and not char.isalnum()
            and char not in ALL_PUNCTUATION
            and char not in already_logged_punctuation
        ):
            log.warning(
                "Unknown punctuation",
                extra={"character": char, "unicode": f"U+{ord(char):04x}"},
            )
            already_logged_punctuation[char] = True

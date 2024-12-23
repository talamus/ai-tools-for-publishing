from libvoikko import Voikko

try:
    VOIKKO = Voikko("fi")
    VOIKKO.setHyphenateUnknownWords(True)
    VOIKKO.setMinHyphenatedWordLength(1)
    VOIKKO.setNoUglyHyphenation(True)
    STRICT_VOIKKO = Voikko("fi")
    STRICT_VOIKKO.setHyphenateUnknownWords(False)
    STRICT_VOIKKO.setMinHyphenatedWordLength(1)
    STRICT_VOIKKO.setNoUglyHyphenation(False)
except Exception:
    raise Exception(
        """Unable to launch Finnish language Voikko

Please make sure that the libvoikko and the
Finnish language dictionary have been installed:

    sudo apt install libvoikko1 voikko-fi\n"""
    )


def get_voikko(allow_unknown: bool = True, min_word_length: int = 1) -> Voikko:
    """Return a Voikko object with the specified settings."""
    global VOIKKO
    VOIKKO.setHyphenateUnknownWords(allow_unknown)
    VOIKKO.setMinHyphenatedWordLength(min_word_length)
    VOIKKO.setNoUglyHyphenation(True)
    return VOIKKO


def get_strict_voikko() -> Voikko:
    """Return a Voikko object that does not hyphenate unknown words."""
    return STRICT_VOIKKO

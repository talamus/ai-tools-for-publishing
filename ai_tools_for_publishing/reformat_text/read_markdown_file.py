import logging
from markdown_it import MarkdownIt
from markdown_it.rules_block.state_block import StateBlock


def custom_plugin(md: MarkdownIt) -> bool:
    """Create a plugin that detects "beats" from Markdown."""

    log = logging.getLogger("beat_plugin")

    def beat(state: StateBlock, startLine: int, endLine: int, silent: bool) -> bool:
        pos = state.bMarks[startLine] + state.tShift[startLine]

        if state.is_code_block(startLine):
            return False

        try:
            marker = state.src[pos : pos + 5]
            if marker != "- - -":
                return False
        except IndexError:
            return False

        log.debug(
            "Beat detected",
            extra={
                "state": state,
                "startLine": startLine,
                "endLine": endLine,
                "silent": silent,
            },
        )

        if silent:
            return True

        level = state.level
        state.line = startLine + 1
        token = state.push("comment", "!-- beat --", 1)
        token.map = [startLine, state.line]
        token.markup = marker
        state.level = level

        return True

    md.block.ruler.before("hr", "beat", beat)


def read_markdown_file(input_file: str) -> str:
    """Read Markdown file."""

    log = logging.getLogger(__name__)

    # Read the file
    log.info("Reading Markdown file %s...", input_file)
    with open(input_file) as file:
        raw = file.read()

    # Return a HTML representation of it
    md = MarkdownIt("commonmark", {"xhtmlOut": False, "typographer": False}).use(
        custom_plugin
    )
    return md.render(raw)

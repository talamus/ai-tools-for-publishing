def guess_html_file_encoding(input_file: str) -> str:
    """Try to guess HTML/XML file encoding."""

    # Gobble up the whole file in binary format
    with open(input_file, "rb") as file:
        binary = file.read()

    # Seek possible encoding definition
    prefixes = (
        b"charset=",
        b"Charset=",
        b"encoding=",
        b"Encoding=",
    )
    start = -1
    for item in prefixes:
        start = binary.find(item)
        if start != -1:
            start += len(item)
            break

    # If none is found, return "utf-8"
    if start == -1:
        return "utf-8"

    # Skip an optional quotation mark
    if binary[start] == ord(b'"') or binary[start] == ord(b"'"):
        start += 1

    # Try to find where the encoding ends
    postfixes = (
        b"'",
        b'"',
        b" ",
        b"\t",
        b"?",
        b"/",
        b">",
    )
    end = start + 40  # No encoding name should be longer than 40 chars...
    for item in postfixes:
        possible_end = binary.find(item, start, end)
        if possible_end == -1:
            continue
        if possible_end < end:
            end = possible_end

    # Good luck...
    return binary[start:end].decode("ascii").strip().lower()

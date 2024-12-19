DEFAULT_CONFIG = {
    "dryrun": False,
    "overwrite": False,
    "min_word_length": 5,
    "allow_unknown": False,
    "list_unknown": False,
    "output_file_extension": "_hyphenated.html",
    "output_xhtml": False,
    "hyphenations_file": None,
    "xhtml_template": """<?xml version="1.0" encoding="UTF-8" ?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{language}" lang="{language}">
<head>
<meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8"/>
<meta name="author" content="{author}"/>
<meta name="copyright" content="{copyright}"/>
<title>{title}</title>
<link type="text/css" rel="stylesheet" href="stylesheet.css"/>
</head>
<body>
{content}
</body>
</html>
""",
}

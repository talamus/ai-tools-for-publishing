DEFAULT_CONFIG = {
    "dry_run": False,
    "overwrite": False,
    "output_name": "{name}{ext}",
    "output_format": "markdown",
    # -----------------------------------------------------------------------------
    "xhtml_template": """<?xml version="1.0" encoding="UTF-8" ?>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{language}">
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
    # -----------------------------------------------------------------------------
    "simplified_html_template": """<!DOCTYPE html>
<html lang="{language}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="author" content="{author}">
<meta name="copyright" content="{copyright}">
</head>
<body>
{content}
</body>
</html>
""",
}

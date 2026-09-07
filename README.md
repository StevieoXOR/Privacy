## `RedactFilepathInsideFile.py`

I built a Python script that reads a PDF file (you specify either the PDF's filepath or a Python `raw text` string of the PDF's raw data contents that you manually provide), and via RegEx the script finds all filepaths *within the file's contents* that start with `C:/Users/` and end with `challenges/`, and then replaces all the characters in between those signals with garbage characters.

This script also works for binary files, allowing 1) usage of regex and 2) printing, with difficult-to-print characters (difficult according to Python at least).

`Why did you replace the filepaths with trash instead of simply deleting the sensitive characters?`
Because PDFs seem to be memory mapped. If a PDF's per-byte mappings are off, the LUT entries in the PDF file become misaligned, causing the PDF to load/render incorrectly, causing once-visible sections to disappear after redaction.

I built this file in a way:
* to be robust to weird usages of slashes and backslashes in a filepath, and
* to warn the redactor/user before the script overwrites and/or corrupts any files (like if you screw up the regex while editing it).

### What you *definitely* need to edit
The filepath of the file you want to redact (at the bottom of the Python file)

### What you *may* need to edit
The RegEx data-finder at the top of the `stripSensitiveFilepath(...)` function, which allows you to configure your starting sentinel and your ending sentinel.

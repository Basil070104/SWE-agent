import argparse

from windowed_file import FileNotOpened, WindowedFile # type: ignore
from flake8_utils import flake8, format_flake8_output # type: ignore

_LINT_ERROR_TEMPLATE = """
Your proposed edit has introduced new syntax error(s). Please read this error message carefully and then retry editing the file.

ERRORS:

{errors}
This is how your edit would have looked if applied
------------------------------------------------
{window_applied}
------------------------------------------------

This is the original code before your edit
------------------------------------------------
{window_original}
------------------------------------------------

Your changes have NOT been applied. Please fix your edit command and try again.
DO NOT re-run the same failed edit command. Running it again will lead to the same error.
"""

_SUCCESS_MSG = "Edit successful."
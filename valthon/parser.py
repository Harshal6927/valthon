from __future__ import annotations

import re
from pathlib import Path

from valthon import VAL2PY_MAPPINGS

"""
Python module for converting valthon code to python code.
"""


def _ends_in_vln(word: str) -> bool:
    """Return True if word ends in .vln, else False.

    Returns:
        boolean: Whether 'word' ends with 'vln' or not

    """
    return word[-3:] == ".vln"


def _change_file_name(name: str, outputname: str | None = None) -> str:
    """Change *.vln filenames to *.py filenames.

    If filename does not end in .vln, it adds .py to the end.

    Returns:
        str: Resulting filename with *.py at the end (unless 'outputname' is
        specified, then that is returned).

    """
    # If outputname is specified, return that
    if outputname is not None:
        return outputname

    # Otherwise, create a new name
    if _ends_in_vln(name):
        return name[:-3] + ".py"

    return name + ".py"


def parse_imports(filename: str) -> list[str]:
    """Parse file for imports and return filenames of imported modules.

    Scan the file to find all import statements and extract the module names.
    Each module name is then appended with ".vln" to represent its valthon file.

    Returns:
        list of str: All imported modules, suffixed with '.vln'. Ie, the name
        the imported files must have if they are valthon files.

    """
    infile_str = ""
    with Path(filename).open(encoding="utf-8") as infile:
        infile_str = infile.read()

    imports = re.findall(r"(?<=import\s)[\w.]+(?=;|\s|$)", infile_str)
    imports2 = re.findall(r"(?<=from\s)[\w.]+(?=\s+import)", infile_str)

    return [im + ".vln" for im in imports + imports2]


def safe_substitute(
    value: str,
    deescaped_key: str,
    line: str,
) -> str:
    """Perform valthon token substitution on a line, ignoring tokens inside strings.

    Returns:
        Code line with safe valthon token substitutions

    """
    string_pattern = r"""
        (?P<string>(['"])(?:\\.|(?!\2).)*\2)  # Match single or double-quoted strings
    """

    def replace_callback(match) -> str:
        if match.group("string"):
            return match.group(0)
        return re.sub(
            rf'(?<!["\'#])\b{re.escape(value)}\b(?!["\'])',
            f"dont_use_{value}_use_{deescaped_key}",
            match.group(0),
        )

    return re.sub(string_pattern, replace_callback, line)


def parse_file(
    filepath: str,
    filename_prefix: str = ".",
    outputname: str | None = None,
    change_imports: dict[str, str] | None = None,
) -> None:
    """Convert a valthon file to a python file and write it to disk."""
    filename = Path(filepath).name

    # Read file to string
    infile_str_raw = ""
    with Path(filepath).open(encoding="utf-8") as infile:
        infile_str_raw = infile.read()

    # Fix indentation
    infile_str_indented = ""
    for line in infile_str_raw.split("\n"):
        # search for comments, and remove for now. Re-add them before writing to

        # result string
        m = re.search(r"[ \t]*(#.*$)", line)

        # make sure # sign is not inside quotations. Delete match object if it is
        if m is not None:
            m2 = re.search(r"[\"'].*#.*[\"']", m.group(0))
            if m2 is not None:
                m = None

        if m is not None:
            add_comment = m.group(0)
            line = re.sub(r"[ \t]*(#.*$)", "", line)
        else:
            add_comment = ""

        # skip empty lines:
        if line.strip() in {"\n", "\r\n", ""}:
            infile_str_indented += add_comment + "\n"
            continue

        # replace anything in mappings.keys() with its value, ignore comments
        # disallow real python
        for key, value in VAL2PY_MAPPINGS.items():
            deescaped_key = key.replace(r"\s+", " ")
            line = safe_substitute(value, deescaped_key, line)
            line = re.sub(rf'(?<!["\'#])\b{key}\b(?!["\'])', value, line)
        infile_str_indented += line + add_comment + "\n"

    # Change imported names if necessary
    if change_imports is not None:
        for module in change_imports:
            infile_str_indented = re.sub(
                rf"(?<=import\\s{module})\\b(?!\\s+as\\b)",
                f"{change_imports[module]} as {module}",
                infile_str_indented,
            )
            infile_str_indented = re.sub(
                f"(?<=from\\s){module}(?=\\s+import)",
                change_imports[module],
                infile_str_indented,
            )

    with Path(filename_prefix + _change_file_name(filename, outputname)).open(
        "w",
        encoding="utf-8",
    ) as outfile:
        outfile.write(infile_str_indented)

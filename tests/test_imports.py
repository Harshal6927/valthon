import os
import subprocess


def test_function() -> None:
    result = subprocess.run(
        ["valthon", "tests/imports.py"],
        stdout=subprocess.PIPE,
        check=False,
    )

    if os.name == "nt":
        assert result.stdout == b"1\r\n"
    else:
        assert result.stdout == b"1\n"

    result = subprocess.run(
        ["valthon", "tests/imports.vln"],
        stdout=subprocess.PIPE,
        check=False,
    )

    if os.name == "nt":
        assert result.stdout == b"1\r\n"
    else:
        assert result.stdout == b"1\n"

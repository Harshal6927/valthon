import os
import subprocess


def test_function() -> None:
    result = subprocess.run(
        ["valthon", "tests/function.py"],
        stdout=subprocess.PIPE,
        check=False,
    )

    if os.name == "nt":
        assert result.stdout == b"Hello World!\r\n"
    else:
        assert result.stdout == b"Hello World!\n"

    result = subprocess.run(
        ["valthon", "tests/function.vln"],
        stdout=subprocess.PIPE,
        check=False,
    )

    if os.name == "nt":
        assert result.stdout == b"Hello World!\r\n"
    else:
        assert result.stdout == b"Hello World!\n"

import os
import subprocess


def test_comments() -> None:
    result = subprocess.run(
        ["valthon", "tests/comments.py"],
        stdout=subprocess.PIPE,
        check=False,
    )

    if os.name == "nt":
        assert result.stdout == b"Hello World!\r\n"
    else:
        assert result.stdout == b"Hello World!\n"

    result = subprocess.run(
        ["valthon", "tests/comments.vln"],
        stdout=subprocess.PIPE,
        check=False,
    )

    if os.name == "nt":
        assert result.stdout == b"Hello World!\r\n"
    else:
        assert result.stdout == b"Hello World!\n"

import subprocess


def test_comments() -> None:
    result = subprocess.run(
        ["valthon", "tests/comments.py"],
        stdout=subprocess.PIPE,
        check=False,
    )
    assert result.stdout == b"Hello World!\n"

    result = subprocess.run(
        ["valthon", "tests/comments.vln"],
        stdout=subprocess.PIPE,
        check=False,
    )
    assert result.stdout == b"Hello World!\n"

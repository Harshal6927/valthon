import subprocess


def test_function() -> None:
    result = subprocess.run(
        ["valthon", "tests/imports.py"],
        stdout=subprocess.PIPE,
        check=False,
    )
    assert result.stdout == b"1\n"

    result = subprocess.run(
        ["valthon", "tests/imports.vln"],
        stdout=subprocess.PIPE,
        check=False,
    )
    assert result.stdout == b"1\n"

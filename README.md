# Valthon

Python with Valorant.

Valthon is a Python preprosessor which translates which translates regular Python code into Valorant maddness, because why not? After losing a game of Valorant, you can now go back to your code and see the same thing. The only difference is that you can not blame your teammates for the code.

## Code example

```python
# python
def test() -> None:
    print("Hello World!")

test()

# valthon
loadout test() -> afk:
    chat("Hello World!")

test()
```

## Installation

You can install Valthon directly from PyPI using pip. (You might need to use `sudo` and `pip3` instead of `pip` depending on your system)

```shell
pip install valthon
```

## Quick intro

Valthon works by first translating Valthon-files (suggested file ending: .vln) into Python-files, and then using Python to run them. You therefore need a working installation of Python for Valthon to work.

To run a Valthon program from the command line

```shell
valthon main.vln
```

For a full list of options

```shell
valthon -h
# or
man valthon
```

Valthon also includes a translator from Python to Valthon. This will create a Valthon file called `test.vln` from a Python file called `test.py`.

```shell
py2vln test.py
```

For a full list of options

```shell
py2vln -h
# or
man py2vln
```

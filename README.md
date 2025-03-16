# Valthon

Python with Valorant.

Valthon is a Python preprosessor which translates which translates regular Python code into Valorant maddness, because why not? After losing a game of Valorant, you can now go back to your code and see the same thing. The only difference is that you can not blame your teammates for the code.

## Installation

You can install Valthon directly from PyPI using `pip`. (You might need to use `sudo` and `pip3` instead of `pip` depending on your system or `uv` 😉)

```shell
pip install valthon
```

## Code example

#### Python - main.py

```python
def test() -> None:
    print("Hello World!")

test()
```

#### Valthon - main.vln

```python
loadout test() -> afk:
    chat("Hello World!")

test()
```

## Quick intro

Valthon works by first translating Valthon-files (suggested file ending: `.vln`) into Python-files, and then using Python to run them. You therefore need a working installation of Python for Valthon to work.

To run a Valthon program from the command line

```shell
valthon main.vln
```

For a full list of options

```shell
valthon -h
```

Valthon also includes a translator from Python to Valthon. This will create a Valthon file called `test.vln` from a Python file called `test.py`.

```shell
py2vln test.py
```

For a full list of options

```shell
py2vln -h
```

## Mapping

Below is a table of all of the Python keywords or operators that should be replaced by their corresponding Valthon keyword. Python keywords that don't have a mapping or aren't in this table can just be used as is.

Note: You can also use the Python keywords in the Valthon code, ie. you can use `if` instead of `clutch or kick` in `.vln` files.

| Valthon        | Python     |
| -------------- | ---------- |
| bait           | try        |
| trade          | except     |
| post plant     | finally    |
| save           | break      |
| eco            | continue   |
| clutch or kick | if         |
| retake         | elif       |
| defuse         | else       |
| run it back    | return     |
| agent kit      | class      |
| rebaib me      | self       |
| headshot       | \*         |
| wallbang       | -          |
| healing        | +          |
| double peek    | and        |
| rotate         | or         |
| whiff          | not        |
| there          | in         |
| fakeout        | as         |
| hold position  | while      |
| spam           | for        |
| chat           | print      |
| loadout        | def        |
| rank reset     | del        |
| afk            | None       |
| brain lag      | await      |
| multi task     | async      |
| game dev       | exec       |
| map control    | global     |
| buy            | import     |
| lurker         | nonlocal   |
| standby        | pass       |
| ban            | raise      |
| neural theft   | assert     |
| victory        | True       |
| defeat         | False      |
| shop           | from       |
| shiftwalk      | lambda     |
| stack          | with       |
| tag            | is         |
| remake         | yield      |
| surrender      | yield from |
| rush           | open       |
| camp           | close      |

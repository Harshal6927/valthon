from pathlib import Path

from setuptools import setup

from valthon import VERSION_NUMBER

long_description = Path("README.md").read_text(encoding="utf-8")

# Install python package, scripts and manual pages
setup(
    name="valthon",
    version=VERSION_NUMBER,
    author="Harshal Laheri",
    author_email="harshal@harshallaheri.me",
    license="MIT",
    description="Python with Valorant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harshal6927/valthon",
    scripts=["scripts/valthon", "scripts/py2vln"],
    data_files=[("man/man1", ["etc/valthon.1", "etc/py2vln.1"])],
    packages=["valthon"],
    zip_safe=False,
)

from __future__ import annotations

import os
import sys
from pathlib import Path

from valthon import parser
from valthon.logger import Logger

"""
Module for handling imports of Valthon files in Python code.
"""


def valthon_import(
    module_name: str,
    global_vars: dict,
    logger: Logger | None = None,
) -> None:
    """Import Valthon files in Python code.

    Example:
    ``` python
    from valthon.importing import valthon_import
    valthon_import("test_module", globals())

    # Now, 'test_module' is available like any other module:
    test_module.func()
    ```

    Raises:
        ImportError: If the module cannot be found or if there's an error during parsing.

    """
    if logger is None:
        logger = Logger()

    logger.log_info(f"Looking for {module_name}.vln")
    path = _locate_module(module_name, logger)

    logger.log_info(f"Parsing {path}")
    try:
        parser.parse_file(
            filepath=path,
            filename_prefix=str(Path(sys.path[0]) / "python_"),
        )

        error_during_parsing = None

    except Exception as e:
        error_during_parsing = e

    if error_during_parsing is not None:
        error_message = f"Error while parsing '{path}': {error_during_parsing}"
        raise ImportError(error_message)
    python_file_path = Path(sys.path[0]) / (
        "python_" + parser._change_file_name(module_name)
    )

    logger.log_info(f"Importing {python_file_path}")

    # Hacky way of doing global imports of general modules inside a function
    exec(f"global {module_name}", global_vars)
    exec(f"import python_{module_name} as {module_name}", global_vars)

    # Cleanup
    logger.log_info(f"Removing {python_file_path}")
    os.remove(python_file_path)


def _locate_module(module_name: str, logger: Logger) -> str:
    """Locate the valthon file for a given module name.

    Returns:
        str: Full path of valthon file associated with module.

    Raises:
        ImportError: If module is not found.

    """
    module_path = None

    for path in sys.path:
        logger.log_info(f"Searching in {path}")

        module_path = _traverse_and_find(module_name, path)

        if module_path is not None:
            logger.log_info(f"Module found at {module_path}")
            break

    if module_path is None:
        raise ImportError(f"Could not find any valthon file for {module_name}")

    return module_path


def _traverse_and_find(module_name: str, directory: str) -> str | None:
    """Traverse a directory (recursively), and look for a file named 'module_name'.vln.

    Returns:
        str: Full path of valthon file associated with module, None if no such
        file is found.

    """
    for rootpath, _, files in os.walk(directory):
        for file in files:
            if file == (module_name + ".vln"):
                return str(Path(rootpath) / file)

    return None

#! /usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

import click

from valthon import VERSION_NUMBER, parser
from valthon.logger import Logger


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(
    version=VERSION_NUMBER,
    prog_name="valthon",
    message="v%(version)s",
)
@click.option("--verbose", is_flag=True, help="Print progress")
@click.option(
    "-c",
    "--compile",
    is_flag=True,
    help="Translate to python only (don't run files)",
)
@click.option("-k", "--keep", is_flag=True, help="Keep generated python files")
@click.option(
    "--python2",
    is_flag=True,
    help="Use python2 instead of python3 (default)",
)
@click.option("-o", "--output", help="Specify name of output file (if -c is present)")
@click.argument("input_file", required=True)
@click.argument("args", nargs=-1)
def main(verbose, compile, keep, python2, output, input_file, args) -> None:
    """Valthon is a python preprosessor that translates valthon files to python."""
    # Create logger
    logger = Logger(verbose)

    # Check for invalid combination of flags
    if output is not None and not compile:
        logger.log_error("Cannot specify output when valthon is not in compile mode")
        sys.exit(1)

    # Where to output files
    if compile or keep:
        # No path prefix
        path_prefix = ""
        logger.log_info("Placing files in this directory")
    else:
        # Prefix with . to hide, also to avoid name conflicts.
        path_prefix = "python_"
        logger.log_info(
            "Placing files in this directory, but prefixing them with python_*",
        )

    # List of all files to translate from valthon to python
    parse_que = []

    # Add all files from cmd line
    parse_que.append(input_file)
    if compile:
        for arg in args:
            parse_que.append(arg)

    # Add all files from imports, and recursively add all imports
    logger.log_info("Scanning for imports")
    i = 0
    while i < len(parse_que):
        try:
            import_files = parser.parse_imports(parse_que[i])
        except FileNotFoundError:
            logger.log_error(f"No file named '{parse_que[i]}'")
            sys.exit(1)

        for import_file in import_files:
            if Path(import_file).is_file() and import_file not in parse_que:
                logger.log_info(f"Adding '{import_file}' to parse que")
                parse_que.append(import_file)

        i += 1

    # Handle import translations
    if not path_prefix:
        import_translations = {}
        for file in parse_que:
            import_translations[file[:-3]] = path_prefix + file[:-3]
    else:
        import_translations = None

    # Parsing files
    current_file_name = None
    try:
        for file in parse_que:
            current_file_name = file
            logger.log_info(f"Parsing '{file}'")

            if output is None:
                outputname = None
            elif Path(output).is_dir():
                new_file_name = parser._change_file_name(os.path.split(file)[1])
                outputname = os.path.join(output, new_file_name)
            else:
                outputname = output

            parser.parse_file(
                file,
                path_prefix,
                outputname,
                import_translations,
            )
    except (TypeError, FileNotFoundError) as e:
        logger.log_error(f"Error while parsing '{current_file_name}'.\n{e!s}")
        # Cleanup
        try:
            for file in parse_que:
                Path(path_prefix + parser._change_file_name(file, None)).unlink(
                    missing_ok=True,
                )
        except Exception as e:
            logger.log_error(f"Failed to delete file: {e}")
            raise e
        sys.exit(1)

    # Stop if we were only asked to translate
    if compile:
        return

    # Run file
    if python2:
        python_commands = ["python2", "py -2", sys.executable]
    else:
        python_commands = ["python3", "python", "py", sys.executable]
        if os.name == "nt":
            python_commands.pop(0)

    filename = Path(input_file).name
    py_file = path_prefix + parser._change_file_name(filename, None)
    args_str = " ".join(arg for arg in args)

    try:
        logger.log_info("Running")
        logger.program_header()

        # Try different Python commands until one works
        success = False
        for cmd in python_commands:
            try:
                if os.name == "nt":
                    result = subprocess.run(
                        f"{cmd} {py_file} {args_str}",
                        shell=True,
                        check=False,
                    )
                else:
                    result = subprocess.run([cmd, py_file, *args], check=False)

                if result.returncode == 0:
                    success = True
                    break
            except Exception:
                continue

        if not success:
            logger.log_error("Could not find a working Python interpreter")

        logger.program_footer()

    except Exception as e:
        logger.log_error("Unexpected error while running Python")
        logger.log_info(f"Reported error message: {e!s}")

    # Delete file if requested
    try:
        if not keep:
            logger.log_info("Deleting files")
            for file in parse_que:
                filename = Path(file).name
                Path(path_prefix + parser._change_file_name(filename, None)).unlink(
                    missing_ok=True,
                )
    except Exception:
        logger.log_error(
            "Could not delete created python files.\nSome garbage may remain in the directory",
        )


if __name__ == "__main__":
    main()

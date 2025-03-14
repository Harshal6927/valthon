import sys


class Logger:
    """Logger class. Writes errors and info to the cmd line."""

    def __init__(self, verbose: bool = False) -> None:
        """Initialize a logger object."""
        self.verbose = verbose

    def log_info(self, text: str) -> None:
        """Log an info line, prefixed with an [i]. If verbose is False, this does nothing."""
        if self.verbose:
            print(f" [i]  {text}")

    def log_warn(self, text: str) -> None:
        """Log a warning, prefixed with an [!]. If verbose is False, this does nothing."""
        if self.verbose:
            print(f" [!]  {text}")

    def program_header(self) -> None:
        """Print a header ment to separate info from compiler from the output of the resulting program. If verbose is False, this does nothing."""
        if self.verbose:
            print("\n---- OUPUT FROM PROGRAM ----\n")

    def program_footer(self) -> None:
        """Print a footer ment to separate the output of the resulting program from the info from compiler. If verbose is False, this does nothing."""
        if self.verbose:
            print("\n----     END  OUPUT     ----\n")

    def log_error(self, text: str) -> None:
        """Log an error.

        This will be printed regardless of the status of the verbose variable.
        """
        print(f"\033[91m\033[1mError:\033[0m {text}", file=sys.stderr)

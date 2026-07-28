"""
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.

Argument Parsing for DigDep CLI
"""

import argparse
from ._version import __version__


DESCRIPTION = "Scan Python projects and inspect import dependencies."
EXAMPLES = """
Examples:
  digdep packages ./myproject
  digdep file-tree ./myproject
  digdep dep-tree ./myproject

Ignore directories:
  digdep file-tree ./myproject --ignore venv __pycache__ tests

Redirect output:
  digdep dep-tree ./myproject > dependencies.txt
"""

def add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments to subparser"""
    parser.add_argument(
        "path",
        help="Path to the Python project.",
    )
    parser.add_argument(
        "-i",
        "--ignore",
        nargs="*",
        default=[],
        metavar="NAME",
        help="Directories or files to ignore.",
    )
    parser.add_argument(
        "-I",
        "--ignore-file",
        metavar="FILE",
        help="Read directories to ignore from a file.",
    )
    parser.add_argument(
        "--type",
        "-t",
        default="all",
        metavar="TYPES",
        help=(
            "Comma-separated dependency types (stdlib, third-party, "
            "local, all). Defaults to 'all'."
        )
    )


parser = argparse.ArgumentParser(
    prog="digdep",
    description=DESCRIPTION,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=EXAMPLES
)

parser.add_argument(
    "-v",
    "--version",
    action="version",
    version=f"%(prog)s {__version__}",
)

subparsers = parser.add_subparsers(
    title="Commands",
    dest="command",
    required=True,
)
packages = subparsers.add_parser(
    "packages",
    help = "List imported packages."
)
add_common_args(packages)

file_tree = subparsers.add_parser(
    "file-tree",
    help="Show the file -> dependency tree."
)
add_common_args(file_tree)

dep_tree = subparsers.add_parser(
    "dep-tree",
    help="Show the dependency -> file tree."
)
add_common_args(dep_tree)


def parse_args() -> argparse.Namespace:
    """Parse arguments"""
    return parser.parse_args()


if __name__ == "__main__":
    pass

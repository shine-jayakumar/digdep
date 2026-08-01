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
  digdep deps ./myproject
  digdep file-tree ./myproject
  digdep dep-tree ./myproject
  digdep unused-imports ./myproject
  digdep file-tree ./myproject -o file_tree.json

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
        "-t",
        "--type",
        default="all",
        metavar="TYPES",
        help=(
            "Comma-separated dependency types (stdlib, third-party, "
            "local, all). Defaults to 'all'."
        )
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="FILE",
        help="Write output to a file."
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
deps = subparsers.add_parser(
    "deps",
    help = "List dependencies."
)
add_common_args(deps)

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

unused_import_tree = subparsers.add_parser(
    "unused-imports",
    help="Show the file -> unused imports tree."
)
add_common_args(unused_import_tree)





def parse_args() -> argparse.Namespace:
    """Parse arguments"""
    return parser.parse_args()


if __name__ == "__main__":
    pass

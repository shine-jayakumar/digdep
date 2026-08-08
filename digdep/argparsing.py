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
  digdep deps ./myproject --tree
  digdep deps ./myproject --tree --reverse
  digdep deps ./myproject --tree -o file_tree.json
  digdep deps ./myproject --tree --unused

Ignore directories:
  digdep deps ./myproject --ignore venv __pycache__ tests

Redirect output:
  digdep deps ./myproject > dependencies.txt
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
deps.add_argument(
    "--tree",
    action="store_true",
    help="Show file to dependency tree"
)
deps.add_argument(
    "--reverse",
    action="store_true",
    help="Show dependency to file tree"
)
deps.add_argument(
    "--unused",
    action="store_true",
    help="Show only unused imports"
)
add_common_args(deps)

#file_tree = subparsers.add_parser(
#    "file-deps",
#    help="Show the file -> dependency tree."
#)
#add_common_args(file_tree)
#
#dep_files = subparsers.add_parser(
#    "dep-files",
#    help="Show the dependency -> file tree."
#)
#add_common_args(dep_files)
#output_type = dep_files.add_mutually_exclusive_group()
#dep_files.add_argument(
#    "-tr",
#    "--tree",
#    action="store_true",
#    help="Show output as tree"
#)
#
#
#
#unused_import_tree = subparsers.add_parser(
#    "unused-imports",
#    help="Show the file -> unused imports tree."
#)
#add_common_args(unused_import_tree)

stats = subparsers.add_parser(
    "stats",
    help="Show dependency statistics."
)
add_common_args(stats)
stats.add_argument(
    "-tn",
    "--topn",
    type=int,
    metavar="NUM",
    help="Select top n dependencies."
)

find_dep = subparsers.add_parser(
    "find-dep",
    help="Find files importing a dependency."
)
find_dep.add_argument(
    "dependency",
    metavar="DEPENDENCY",
    help="Name of the dependency to look for."
)
find_dep.add_argument(
    "--tree",
    action="store_true",
    help="Show files with dependency as tree."
)
find_dep.add_argument(
    "-sl",
    "--showlines",
    action="store_true",
    help="Show lines with dependency."
)
add_common_args(find_dep)

def parse_args() -> argparse.Namespace:
    """Parse arguments"""
    return parser.parse_args()


if __name__ == "__main__":
    pass

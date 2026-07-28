"""
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.

DigDep CLI 
"""

import sys
from .argparsing import parse_args
from .analyzer import DepAnalyzer, DepType


ARG_DEPTYPE_MAP = {
    "stdlib": DepType.STDLIB,
    "third-party": DepType.THIRD_PARTY,
    "local": DepType.LOCAL,
    "all": DepType.ALL,
}


def main(is_ascii: bool = False):

    args = parse_args()

    depanalyzer = DepAnalyzer(is_ascii=is_ascii)
    depanalyzer.ignore(args.ignore)
    if args.ignore_file:
        depanalyzer.ignore_from_file(args.ignore_file)
    depanalyzer.scan(args.path)

    arg_deptypes = args.type.split(",")
    invalid_types = set(arg_deptypes).difference(ARG_DEPTYPE_MAP.keys())
    if invalid_types:
        invalid_types = ", ".join(invalid_types)
        print(f"Error: Invalid dependency type - {invalid_types}")
        sys.exit(1)

    filters = DepType.NONE
    for deptype in arg_deptypes:
        filters |= ARG_DEPTYPE_MAP.get(deptype.strip(), DepType.NONE)
    filters = DepType.ALL if filters == DepType.NONE else filters

    if args.command == "packages":
        depanalyzer.show_packages(filters=filters)
    elif args.command == "file-tree":
        depanalyzer.file_dependency_tree(filters=filters)
    elif args.command == "dep-tree":
        depanalyzer.dependency_file_tree(filters=filters)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    is_ascii = False if sys.stdout.isatty() else True
    main(is_ascii)


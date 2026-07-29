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
from collections.abc import Callable
from .exceptions import *


ARG_DEPTYPE_MAP = {
    "stdlib": DepType.STDLIB,
    "third-party": DepType.THIRD_PARTY,
    "local": DepType.LOCAL,
    "all": DepType.ALL,
}


def get_filters(args) -> DepType:
    """Get filters from arguments"""
    arg_deptypes = args.type.split(",")
    invalid_types = set(arg_deptypes).difference(ARG_DEPTYPE_MAP.keys())
    if invalid_types:
        invalid_types = ", ".join(invalid_types)
        raise DependencyTypeError(f"Invalid dependency type - {invalid_types}")

    filters = DepType.NONE
    for deptype in arg_deptypes:
        filters |= ARG_DEPTYPE_MAP.get(deptype.strip(), DepType.NONE)
    filters = DepType.ALL if filters == DepType.NONE else filters
    return filters


def process_command(args, analyzer: DepAnalyzer) -> None:
    """Process the command in args"""
    cmd = args.command.replace("-", "_")
    output_type = (
        args.output.split(".")[-1].strip().lower() if args.output
        else ""
    )
    if output_type and output_type not in ("json",):
        raise OutputTypeError(f"Output type '{output_type}' is not supported")

    funcname = f"show_{cmd}"
    filters = get_filters(args)
    kwargs = {"filters": filters}
    if output_type:
        funcname = f"{cmd}_{output_type}"
        kwargs["fpath"] = args.output
    func = getattr(analyzer, funcname, None)
    if not callable(func):
        raise CLICommandError("Invalid command '{args.command}'")
    func(**kwargs)


def main(is_ascii: bool = False):

    args = parse_args()

    depanalyzer = DepAnalyzer(is_ascii=is_ascii)
    depanalyzer.ignore(args.ignore)
    if args.ignore_file:
        depanalyzer.ignore_from_file(args.ignore_file)
    depanalyzer.scan(args.path)

    try:
        process_command(args, depanalyzer)
    except DigDepException as ex:
        print(f"Error: {str(ex)}")
    except Exception as ex:
        print(f"Program Error: {str(ex)}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    is_ascii = False if sys.stdout.isatty() else True
    main(is_ascii)


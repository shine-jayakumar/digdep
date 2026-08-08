"""
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.

DigDep CLI 
"""

import sys
from .argparsing import parse_args, parser
from .analyzer import DepAnalyzer, DepType
from collections.abc import Callable
from .exceptions import *
from .cli_dispatcher import Dispatcher


def main(is_ascii: bool = False):

    try:
        args = parse_args()
        config = {"is_ascii": is_ascii}
        try:
            dispatcher = Dispatcher(args, config)
            dispatcher.run_command()
        except DigDepException as dex:
            if isinstance(dex, (CommandNotMappedError, InvalidArgumentError)):
                raise dex
            print(f"Error: {str(dex)}")
    except InvalidArgumentError as parser_ex:
        parser.error(str(parser_ex))
    #except Exception as ex:
    #    print(f"Program Error: {str(ex)}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    is_ascii = False if sys.stdout.isatty() else True
    main(is_ascii)


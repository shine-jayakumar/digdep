"""
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.

CLI Dispatcher
"""

from typing import TypeAlias, Callable
from .analyzer import DepAnalyzer, DepType
from .command_handlers import *
from .cli_options import *
from .exceptions import *


Command: TypeAlias = str


class Dispatcher:

    def __init__(self, args, config: dict):
        self._args = args
        self._config = config
        self._analyzer = None
        self._common_clioptions: tuple[CLIOption] = (
            Path, Ignore, IgnoreFile, 
        )
        self._cmd_handler_map: dict[Command, CommandHandler] = {
            "deps": Deps,
            "stats": Stats,
            "find-dep": FindDep
        }
        self._init_analyzer()

    def _init_analyzer(self) -> None:
        """Initialize analyzer with common cli options"""
        is_ascii = self._config.get("is_ascii", False)
        self._analyzer = DepAnalyzer(is_ascii=is_ascii)
        for option in self._common_clioptions:
            func = getattr(self._analyzer, option.analyzer_funcname, None)
            if not func:
                raise InvalidAnalyzerFunctionError(
                    f"Invalid analyzer function - '{option.analyzer_funcname}'"
                )
            argname, argval = option(self._args).to_argval()
            if not argval:
                continue
            func(**{argname: argval})

    def run_command(self) -> None:
        """Call function mapped to the command"""
        command = self._args.command
        handler = self._cmd_handler_map.get(command)
        if not handler:
            raise CommandNotMappedError(
                f"Command '{command}' is not mapped to a function"
            )
        handler = handler(self._args, self._analyzer) 
        handler.run()


if __name__ == "__main__":
    pass
   

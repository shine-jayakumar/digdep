"""
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.

CLI Options
"""

from dataclasses import dataclass
from .analyzer import DepType
from typing import Any
from .exceptions import *


class CLIOption:

    option: str
    analyzer_argname: str
    analyzer_funcname: str

    def __init__(self, args):
        self._args = args

    def to_argval(self) -> tuple[str, Any]:
        """Generate analyzer analyzer_argname and value"""
        optval = getattr(self._args, self.__class__.option, None)
        return (self.__class__.analyzer_argname, optval)


class Ignore(CLIOption):

    option = "ignore"
    analyzer_argname = "ignorelist"
    analyzer_funcname = "ignore"


class IgnoreFile(CLIOption):

    option = "ignore_file"
    analyzer_argname = "fpath"
    analyzer_funcname = "ignore_from_file"


class Path(CLIOption):

    option = "path"
    analyzer_argname = "root"
    analyzer_funcname = "analyze"


class Output(CLIOption):

    option = "output"
    analyzer_argname: str = "fpath"


class Tree(CLIOption):

    option = "tree"
    analyzer_argname: str = "tree"


class Reverse(CLIOption):

    option = "reverse"
    analyzer_argname: str = "reverse"


class Unused(CLIOption):

    option = "unused"
    analyzer_argname: str = "unused"


class TopN(CLIOption):

    option = "topn"
    analyzer_argname: str = "topn"


class Dependency(CLIOption):

    option = "dependency"
    analyzer_argname = "dependency"


class ShowLines(CLIOption):

    option = "showlines"
    analyzer_argname = "showlines"


class DepFilter(CLIOption):

    option = "type"
    analyzer_argname = "filters"

    def to_argval(self):
        deptype_map = {
            "stdlib": DepType.STDLIB,
            "third-party": DepType.THIRD_PARTY,
            "local": DepType.LOCAL,
            "all": DepType.ALL,
        }
        if not hasattr(self._args, self.option):
            return (self.analyzer_argname, DepType.ALL)
        deptypes = getattr(self._args, self.__class__.option, "")
        deptypes = deptypes.split(",") if deptypes else []
        invalid_types = set(deptypes).difference(deptype_map.keys())
        if invalid_types:
            invalid_types = ", ".join(invalid_types)
            raise DependencyTypeError(
                f"Invalid dependency type - {invalid_types}"
            )
        filters = DepType.NONE
        for deptype in deptypes:
            filters |= deptype_map.get(deptype.strip(), DepType.NONE)
        filters = DepType.ALL if filters == DepType.NONE else filters
        return (self.__class__.analyzer_argname, filters)


if __name__ == "__main__":
    pass

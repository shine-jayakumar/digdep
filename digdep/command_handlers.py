"""
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.

Command Handlers for CLI options
"""

from abc import ABC, abstractmethod
from enum import Flag, auto
from .analyzer import DepAnalyzer
from .cli_options import *


class CommandHandler(ABC):

    options: tuple[CLIOption]

    def __init__(self, args, analyzer: DepAnalyzer) -> None:
        self._args = args
        self._analyzer = analyzer
        self._kwargs = {}
        self._validate_args()
        self._parse_args()

    def _validate_args(self) -> None:
        """Validate arguments"""
        pass

    def _parse_args(self) -> None:
        for option in self.__class__.options:
            argname, argval = option(self._args).to_argval()
            self._kwargs[argname] = argval

    @abstractmethod
    def run(self) -> None:
        """Run analyzer function"""
        ...


class Deps(CommandHandler):

    options = (DepFilter, Tree, Reverse, Unused, Output)

    class Mode(Flag):
        Flat = 0
        Tree = auto()
        File = auto()
        Unused = auto()
        Reverse = auto()

    def __init__(self, args, analyzer) -> None:
        super().__init__(args, analyzer)

        self._mode_func_map = {
            self.Mode.Flat: self._deps_flat,
            self.Mode.Flat | self.Mode.File: self._deps_flat_json,
            self.Mode.Tree: self._deps_tree,
            self.Mode.Tree | self.Mode.File: self._deps_tree_json,
            self.Mode.Tree | self.Mode.Reverse: self._deps_tree_reverse,
            self.Mode.Tree | self.Mode.Reverse | self.Mode.File: (
                self._deps_tree_reverse_json
            ),
            self.Mode.Unused: self._deps_unused_flat,
            self.Mode.Unused | self.Mode.File: self._deps_unused_flat_json,
            self.Mode.Unused | self.Mode.Tree: self._deps_unused_tree,
            self.Mode.Unused | self.Mode.Tree | self.Mode.File: (
                self._deps_unused_tree_json
            )
        }

    def _validate_args(self) -> None:
        """Validate arguments"""
        if self._args.reverse and not self._args.tree:
            raise InvalidArgumentError(
                f"--reverse cannot be used without --tree"
            )

        if self._args.reverse and self._args.unused:
            raise InvalidArgumentError(
                f"--reverse cannot be used with --unused"
            )

    def _deps_flat(self, filters: DepType, **kwargs) -> None:
        self._analyzer.show_deps(filters=filters)
    
    def _deps_flat_json(self, fpath: str, filters: DepType, **kwargs) -> None:
        self._analyzer.deps_json(fpath=fpath, filters=filters)

    def _deps_tree(self, filters: DepType, **kwargs) -> None:
        self._analyzer.show_filedep_tree(filters=filters)

    def _deps_tree_json(self, fpath: str, filters: DepType, **kwargs) -> None:
        self._analyzer.filedep_tree_json(fpath=fpath, filters=filters)

    def _deps_tree_reverse(self, filters: DepType, **kwargs) -> None:
        self._analyzer.show_depfiles_tree(filters=filters)

    def _deps_tree_reverse_json(
        self, fpath: str, filters: DepType, **kwargs
    ) -> None:
        self._analyzer.depfiles_tree_json(fpath=fpath, filters=filters)

    def _deps_unused_flat(self, **kwargs) -> None:
        self._analyzer.show_unused_imports()

    def _deps_unused_flat_json(self, fpath: str, **kwargs) -> None:
        self._analyzer.unused_imports_json(fpath=fpath)

    def _deps_unused_tree(self, **kwargs) -> None:
        self._analyzer.show_unused_imports_tree()

    def _deps_unused_tree_json(self, fpath: str, **kwargs) -> None:
        self._analyzer.unused_imports_tree_json(fpath=fpath)

    def run(self) -> None:
        """Run analyzer function"""
        filters = self._kwargs.get("filters")
        tree = self._kwargs.get("tree")
        fpath = self._kwargs.get("fpath")
        reverse = self._kwargs.get("reverse")
        unused = self._kwargs.get("unused")

        flags = self.Mode.Tree if tree else self.Mode.Flat
        if fpath:
            flags |= self.Mode.File
        if reverse:
            flags |= self.Mode.Reverse
        if unused:
            flags |= self.Mode.Unused

        func = self._mode_func_map.get(flags)
        if not func:
            raise CommandNotMappedError(
                f"Command not mapped for mode '{flags}'"
            )
        func(filters=filters, fpath=fpath)


class Stats(CommandHandler):

    options = (TopN,)
    
    def run(self) -> None:
        topn = self._kwargs.get("topn")
        topn = topn if topn else 5
        self._analyzer.show_stats(topn=topn)


class FindDep(CommandHandler):

    options = (Dependency, Tree, ShowLines, Output)

    class Mode(Flag):
        Flat = 0
        Tree = auto()
        File = auto()

    def __init__(self, args, analyzer: DepAnalyzer) -> None:
        super().__init__(args, analyzer)
        self._mode_func_map = {
            self.Mode.Flat: self._finddep_flat,
            self.Mode.Flat | self.Mode.File: self._finddep_flat_json,
            self.Mode.Tree: self._finddep_tree,
            self.Mode.Tree | self.Mode.File: self._finddep_tree_json
        }

    def _validate_args(self) -> None:
        if self._args.showlines and not self._args.tree:
            raise InvalidArgumentError(
                f"--showlines cannot be used without --tree"
            )

    def _finddep_flat(self, dependency: str, **kwargs) -> None:
        self._analyzer.show_files_with_dep(dependency=dependency)

    def _finddep_flat_json(
        self, fpath: str, dependency: str, **kwargs
    ) -> None:
        self._analyzer.files_with_dep_json(fpath=fpath, dependency=dependency)

    def _finddep_tree(
        self, dependency: str, showlines: bool = False, **kwargs
    ) -> None:
        self._analyzer.show_files_with_dep_tree(
            dependency=dependency, showlines=showlines
        )

    def _finddep_tree_json(
        self, fpath: str, dependency: str, showlines: bool = False, **kwargs
    ) -> None:
        self._analyzer.files_with_dep_tree_json(
            fpath=fpath, dependency=dependency, showlines=showlines
        )

    def run(self) -> None:
        dependency = self._kwargs.get("dependency")
        tree = self._kwargs.get("tree")
        fpath = self._kwargs.get("fpath")
        showlines = self._kwargs.get("showlines")
        flags = self.Mode.Tree if tree else self.Mode.Flat
        if fpath:
            flags |= self.Mode.File

        func = self._mode_func_map.get(flags)
        if not func:
            raise CommandNotMappedError(
                f"Command not mapped for mode '{flags}'"
            )
        func(fpath=fpath, dependency=dependency, showlines=showlines)


if __name__ == "__main__":
    pass

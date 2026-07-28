"""
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.

Core dependency analyzer
"""

import ast
from pathlib import Path
from rich.console import Console
from enum import Flag, auto
import sys
from .visitors import DependencyVisitor
from .utils import walkpath


class DepType(Flag):
    NONE = 0
    STDLIB = auto()
    THIRD_PARTY = auto()
    LOCAL = auto()
    UNKNOWN = auto()
    ALL = STDLIB | THIRD_PARTY | LOCAL


class DepAnalyzer:

    def __init__(self, is_ascii: bool = False) -> None:
        self._root: Path = None
        self._filedep_tree = {}
        self._depfile_tree = {}
        self._dep_type_map: dict[str, DepType] = {}
        self._ignorelist: set[str] = set()
        self._path_dep_map: dict[Path, set[str]] = {}
        self._is_ascii: bool = is_ascii
        self._tree_prefix_char = (
            "├──" if not self._is_ascii else "|__"
        )
        self._console = Console()

    def ignore(self, ignorelist: list[str]) -> None:
        """Adds files/directories to ignorelist"""
        self._ignorelist = set(ignorelist)

    def ignore_from_file(self, fpath: str) -> None:
        """Read directories to ignore from a file"""
        try:
            with open(fpath, "r") as fh:
                dirnames = [line.strip() for line in fh if line.strip()]
                self._ignorelist.update(dirnames)
        except Exception as ex:
            print(
                (
                    f"Error: Failed to read: {fpath}\n"
                    f"{ex.__class__.__name__} - {str(ex)}"
                )
            )

    @property
    def ignorelist(self) -> tuple[str]:
        """Get ignored directories"""
        return tuple(self._ignorelist)

    def _get_file_deps(self, fpath: str) -> list[str]:
        """Get dependencies in a file"""
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                source = fh.read()
                tree = ast.parse(source)
                visitor = DependencyVisitor()
                visitor.visit(tree)
                return visitor.packages
        except Exception as ex:
            print(
                (
                    f"Failed to read: {fpath}\n"
                    f"{ex.__class__.__name__} - {str(ex)}"
                )
            )
        return []

    def _get_deptype(self, dep: str) -> DepType:
        """Get the dependency type"""
        if dep in sys.stdlib_module_names:
            return DepType.STDLIB
        return DepType.THIRD_PARTY

    def _update_deptype_map(self, deps: set[str]) -> None:
        """Update dependency in dependency-type mapping"""
        new_deps = deps.difference(self._dep_type_map.keys())
        self._dep_type_map.update({
            dep: self._get_deptype(dep) for dep in new_deps
        })

    def _reset_vars(self) -> None:
        """Resets variables"""
        self._filedep_tree = {}
        self._depfile_tree = {}
        self._dep_type_map = {}
        self._path_dep_map = {}

    def scan(self, root: str = ".") -> None:
        """Scans a python file(s) in a directory/sub-directory"""
        self._reset_vars()
        self._root = Path(root)
        for path in walkpath(root, self._ignorelist):
            deps = self._get_file_deps(str(path.resolve()))
            deps = set(deps) if deps else set()
            relpath =  path.relative_to(self._root)
            self._path_dep_map[relpath] = deps
            self._update_deptype_map(deps)

    def get_packages(self, filters: DepType = DepType.ALL) -> tuple[str]:
        deps = self._get_filtered_deps(filters) 
        return tuple(deps)

    def show_packages(self, filters: DepType = DepType.ALL) -> None:
        print("\n".join(dep for dep in self.get_packages(filters)))

    def _tree_prefix(self, indent: int = 0) -> str:
        """Generates tree prefix with indentation"""
        spaces = " " * indent
        return f"{spaces}{self._tree_prefix_char}"

    def _vertical_spacer(self, indent: int = 0) -> str:
        """Generates a vertical spacer"""
        spaces = " " * indent
        return f"{spaces}|"

    def _print(self, text: str) -> None:
        """Coloured print"""
        self._console.print(text)

    def _gen_filedeps_tree(self) -> None:
        """Generate file dependency tree"""
        if self._filedep_tree:
            return self._filedep_tree
        self._filedep_tree = {"files": []}
        for path, deps in self._path_dep_map.items():
            dirparts = path.parent.parts
            branch = self._filedep_tree
            for part in dirparts:
                branch = branch.setdefault(part, {"files": []})
            branch["files"].append((path.name, deps))

    def _gen_depfiles_tree(self) -> None:
        """Generate dependency file tree"""
        if self._depfile_tree:
            return self._depfile_tree
        self._depfile_tree = {}
        for path, deps in self._path_dep_map.items():
            dirparts = path.parent.parts
            for dep in deps:
                branch = self._depfile_tree.setdefault(dep, {"files": []})
                for part in dirparts:
                    branch = branch.setdefault(part, {"files": []})
                branch["files"].append(path.name)

    def _get_filtered_deps(self, filters: DepType) -> set[str]:
        """Filter dependencies by type"""
        return {
            dep
            for dep, deptype in self._dep_type_map.items()
            if filters & deptype
        }

    def get_filedep_tree(self, filters: DepType = DepType.ALL) -> dict:
        """Get the file-dependency tree"""
        self._gen_filedeps_tree()
        return self._filedep_tree

    def file_dependency_tree(self, filters: DepType = DepType.ALL) -> None:
        """Show file and dependencies"""
        self._gen_filedeps_tree()
        relevant_deps = (
            self._get_filtered_deps(filters) if filters else set()
        )
        def showdep(branch: dict, indent=0):
            files = branch.get("files", [])
            tree_prefix = self._tree_prefix(indent)
            maxwidth = (
                max(len(file) for file, _ in files) if files else 0
            )
            for file, deps in files:
                deps = deps.intersection(relevant_deps)
                deps = ", ".join(sorted(deps))
                deps = f" → [bold cyan]{deps}[/bold cyan]" if deps else ""
                self._print(f"{tree_prefix} {file:<{maxwidth}}{deps}")

            dirs = {k:v for k,v in branch.items() if isinstance(v, dict)}
            for _dir, val in dirs.items():
                print(self._vertical_spacer(indent))
                self._print(f"{tree_prefix} [blue]{_dir}[/blue]/")
                showdep(val, indent + 4)

        self._print(f"[bold magenta]Root ({self._root})[/bold magenta]")
        showdep(self._filedep_tree)

    def get_depfile_tree(self, filters: DepType = DepType.ALL) -> dict:
        """Get the dependency-file tree"""
        self._gen_depfiles_tree()
        return self._depfile_tree

    def dependency_file_tree(self, filters: DepType = DepType.ALL) -> None:
        """Show dependency and files"""
        self._gen_depfiles_tree()
        relevant_deps = (
            self._get_filtered_deps(filters) if filters else set()
        )
        def showfiles(branch: dict, indent=0):
            files = branch.get("files", [])
            tree_prefix = self._tree_prefix(indent)
            for file in files:
                print(f"{tree_prefix} {file}")

            dirs = {k:v for k,v in branch.items() if isinstance(v, dict)}
            for _dir, val in dirs.items():
                print(self._vertical_spacer(indent))
                self._print(f"{tree_prefix} [blue]{_dir}[/blue]/")
                showfiles(val, indent + 4)

        filtered_deps = (
            set(self._depfile_tree.keys()).intersection(relevant_deps)
        )
        for dep in filtered_deps:
            deptree = self._depfile_tree.get(dep)
            self._print(f"[bold cyan]{dep}[/bold cyan]")
            showfiles(deptree)
            print("\n")


if __name__ == "__main__":
    pass

    




        





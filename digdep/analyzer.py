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
from rich.text import Text
from rich.syntax import Syntax
from enum import Flag, auto
import sys
import json
from dataclasses import dataclass, field
from collections import Counter
from linecache import getline
import re
from .visitors import DependencyVisitor, Dependency
from .utils import walkpath
from .exceptions import *


class DepType(Flag):
    NONE = 0
    STDLIB = auto()
    THIRD_PARTY = auto()
    LOCAL = auto()
    UNKNOWN = auto()
    ALL = STDLIB | THIRD_PARTY | LOCAL


@dataclass
class Stats:
    files: int = 0
    imported_names: int = 0
    import_statements: int = 0
    unique_deps: int = 0
    used_imports: int = 0
    unused_imports: int = 0
    stdlib: int = 0
    third_party: int = 0
    local: int = 0
    _dep_count_map: dict[str, int] = field(default_factory=dict)

    def update_dep_count(self, dep_count: dict[str, int]):
        self._dep_count_map.update(dep_count)

    def get_top_deps(self, n:int):
        top_deps = sorted(
            ((dep, count) for dep, count in self._dep_count_map.items()),
            key=lambda v: v[1], reverse=True
        )
        return top_deps[:n]
    

class DepAnalyzer:

    def __init__(self, is_ascii: bool = False) -> None:
        self._root: Path = None
        self._filesdep_tree = {}
        self._depfiles_tree = {}
        self._unused_import_tree = {}
        self._files_with_dep_tree = {}
        self._dep_type_map: dict[str, DepType] = {}
        self._ignorelist: set[str] = set()
        self._path_unique_dep_map: dict[Path, set[str]] = {}
        self._path_unused_import_map: dict[Path, set[str]] = {}
        self._path_dependency_map: dict[Path, list[Dependency]] = {}
        self._local_deps: set[str] = set()
        self._unused_deps: set[str] = set()
        self._stats: Stats = Stats()
        self._is_ascii: bool = is_ascii
        self._tree_prefix_char = (
            "├──" if not self._is_ascii else "|__"
        )
        self._vertical_space_char = (
            "│" if not self._is_ascii else "|"
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

    @property
    def stats(self):
        return self._stats

    def _get_file_deps(self, fpath: str) -> list[tuple[str, int]]:
        """Get dependencies in a file"""
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                source = fh.read()
                tree = ast.parse(source)
                visitor = DependencyVisitor()
                visitor.visit(tree)
                return visitor.deps
        except Exception as ex:
            print(
                (
                    f"Failed to read: {fpath}\n"
                    f"{ex.__class__.__name__} - {str(ex)}"
                )
            )
        return []

    def _get_visitor(self, fpath: str) -> DependencyVisitor:
        """DependencyVisitor for source code in fpath"""
        with open(fpath, "r", encoding="utf-8") as fh:
            source = fh.read()
            tree = ast.parse(source)
            visitor = DependencyVisitor()
            visitor.visit(tree)
            return visitor
        
    def _get_deptype(self, dep: str) -> DepType:
        """Get the dependency type"""
        if dep in sys.stdlib_module_names:
            return DepType.STDLIB
        if dep in self._local_deps:
            return DepType.LOCAL
        return DepType.THIRD_PARTY

    def _update_deptype_map(self, deps: set[str]) -> None:
        """Update dependency in dependency-type mapping"""
        new_deps = deps.difference(self._dep_type_map.keys())
        self._dep_type_map.update({
            dep: self._get_deptype(dep) for dep in new_deps
        })

    def _reset_vars(self) -> None:
        """Resets variables"""
        self._filesdep_tree = {}
        self._depfiles_tree = {}
        self._dep_type_map = {}
        self._path_unique_dep_map = {}
        self._local_deps = set()
        self._path_dependency_map = {}

    def _update_stats_unique_dep_count(self) -> None:
        """Update stats unique deps"""
        self._stats.unique_deps = len(self._dep_type_map)

    def _update_stats_deptype_count(self) -> None:
        """Updates stats dependency types count"""
        typecount = Counter(
            deptype for deptype in self._dep_type_map.values()
        )
        self._stats.stdlib = typecount.get(DepType.STDLIB, 0)
        self._stats.third_party = typecount.get(DepType.THIRD_PARTY, 0)
        self._stats.local = typecount.get(DepType.LOCAL, 0)

    def _update_stats(
        self, visitor: DependencyVisitor, nfiles: int = 1
    ) -> None:
        """Update stats"""
        self._stats.files += nfiles
        self._stats.import_statements += visitor.import_statements
        self._stats.imported_names += len(visitor.import_names)
        self._stats.used_imports += visitor.used_imports_count
        self._stats.unused_imports += visitor.unused_imports_count

        dep_count = Counter(dep.module for dep in visitor.deps)
        self._stats.update_dep_count(dict(dep_count))

    def analyze(self, root: str = ".") -> None:
        """Scans a python file(s) in a directory/sub-directory"""
        self._reset_vars()
        self._root = Path(root)
        self._stats = Stats()
        for path in walkpath(root, self._ignorelist):
            visitor = self._get_visitor(str(path.resolve()))
            deps = visitor.deps
            if deps:
                self._local_deps.update(dep.module for dep in deps if dep.level > 0)
            unique_deps = set(dep.module for dep in deps)
            relpath =  path.relative_to(self._root)
            self._path_unique_dep_map[relpath] = unique_deps
            self._update_deptype_map(unique_deps)
            self._path_unused_import_map[relpath] = visitor.unused_imports
            self._unused_deps.update(visitor.unused_imports)
            self._path_dependency_map[relpath] = deps

            self._update_stats(visitor)

        self._update_stats_unique_dep_count()
        self._update_stats_deptype_count()

    def get_deps(self, filters: DepType = DepType.ALL) -> tuple[str]:
        deps = self._get_filtered_deps(filters) 
        return tuple(deps)

    def deps_json(self, fpath: str, filters: DepType = DepType.ALL) -> str | None:
        """Dump dependencies to json"""
        deps = self._get_filtered_deps(filters)
        json_deps = {"dependencies": list(deps)}
        if fpath:
            json.dump(json_deps, open(fpath, "w"), indent=4)
            return None
        return json.dumps(json_deps, indent=4)

    def show_deps(self, filters: DepType = DepType.ALL) -> None:
        print("\n".join(dep for dep in self.get_deps(filters)))

    def _tree_prefix(self, indent: int = 0) -> str:
        """Generates tree prefix with indentation"""
        spaces = " " * indent
        return f"{spaces}{self._tree_prefix_char}"

    def _vertical_spacer(self, indent: int = 0) -> str:
        """Generates a vertical spacer"""
        spaces = " " * indent
        return f"{spaces}{self._vertical_space_char}"

    def _print(self, text: str) -> None:
        """Coloured print"""
        self._console.print(text)

    def _gen_filedeps_tree(self) -> None:
        """Generate file dependency tree"""
        if self._filesdep_tree:
            return self._filesdep_tree
        self._filesdep_tree = {"files": []}
        for path, deps in self._path_unique_dep_map.items():
            dirparts = path.parent.parts
            branch = self._filesdep_tree
            for part in dirparts:
                branch = branch.setdefault(part, {"files": []})
            branch["files"].append((path, deps))

    def _gen_depfiles_tree(self) -> None:
        """Generate dependency file tree"""
        if self._depfiles_tree:
            return self._depfiles_tree
        self._depfiles_tree = {}
        for path, deps in self._path_unique_dep_map.items():
            dirparts = path.parent.parts
            for dep in deps:
                branch = self._depfiles_tree.setdefault(dep, {"files": []})
                for part in dirparts:
                    branch = branch.setdefault(part, {"files": []})
                branch["files"].append(path)

    def _gen_unused_import_tree(self) -> None:
        """Generate unused import tree"""
        if self._unused_import_tree:
            return self._unused_import_tree
        self._unused_import_tree = {"files": []}
        for path, unused_imports in self._path_unused_import_map.items():
            dirparts = path.parent.parts
            branch = self._unused_import_tree
            for part in dirparts:
                branch = branch.setdefault(part, {"files": []})
            branch["files"].append((path, unused_imports))

    def _get_filtered_deps(self, filters: DepType = DepType.ALL) -> set[str]:
        """Filter dependencies by type"""
        return {
            dep
            for dep, deptype in self._dep_type_map.items()
            if filters & deptype
        }

    def get_file_tree(self, filters: DepType = DepType.ALL) -> dict:
        """Get the file-dependency tree"""
        self._gen_filedeps_tree()
        return self._filesdep_tree

    def filedep_tree_json(
        self, fpath: str, filters: DepType = DepType.ALL
    ) -> str | None:
        """Dump File-Dependency tree to json"""
        self._gen_filedeps_tree()
        relevant_deps = (
            self._get_filtered_deps(filters) if filters else set()
        )
        json_tree = {}

        def copytree(src_branch: dict, dst_branch: dict):
            path_deps = src_branch.get("files", [])
            dst_branch["files"] = {}
            for path, deps in path_deps:
                deps = deps.intersection(relevant_deps)
                dst_branch["files"][path.name] = sorted(deps)

            dirs = {k:v for k,v in src_branch.items() if isinstance(v, dict)}
            for _dir, val in dirs.items():
                dst_branch[_dir] = {}
                copytree(val, dst_branch[_dir])

        copytree(self._filesdep_tree, json_tree)
        if fpath:
            json.dump(json_tree, open(fpath, "w"), indent=4)
            return
        return json.dumps(json_tree, ident=4)

    def show_filedep_tree(self, filters: DepType = DepType.ALL) -> None:
        """Show file and dependencies"""
        self._gen_filedeps_tree()
        relevant_deps = (
            self._get_filtered_deps(filters) if filters else set()
        )
        def showdep(branch: dict, indent=0):
            path_deps = branch.get("files", [])
            tree_prefix = self._tree_prefix(indent)
            maxwidth = (
                max(len(path.name) for path, _ in path_deps) 
                if path_deps else 0
            )
            for path, deps in path_deps:
                deps = deps.intersection(relevant_deps)
                deps = ", ".join(sorted(deps))
                deps = f" → [bold cyan]{deps}[/bold cyan]" if deps else ""
                self._print(f"{tree_prefix} {path.name:<{maxwidth}}{deps}")

            dirs = {k:v for k,v in branch.items() if isinstance(v, dict)}
            for _dir, val in dirs.items():
                print(self._vertical_spacer(indent))
                self._print(f"{tree_prefix} [blue]{_dir}[/blue]/")
                showdep(val, indent + 4)

        self._print(f"[bold magenta]Root ({self._root})[/bold magenta]")
        showdep(self._filesdep_tree)

    def get_depfiles_tree(self, filters: DepType = DepType.ALL) -> dict:
        """Get the dependency-file tree"""
        self._gen_depfiles_tree()
        return self._depfiles_tree

    def depfiles_tree_json(
        self, fpath: str, filters: DepType = DepType.ALL
    ) -> str | None:
        """Dump Dependency-File tree to json"""
        def convert_tree(tree):
            newtree = {}
            newtree["files"] = [path.name for path in tree.get("files", [])]
            dirnames = [
                dirname for dirname, val in tree.items()
                if isinstance(val, dict)
            ]
            for dirname in dirnames:
                newtree[dirname] = convert_tree(tree.get(dirname))
            return newtree
            
        self._gen_depfiles_tree()
        relevant_deps = (
            self._get_filtered_deps(filters) if filters else set()
        )
        filtered_deps = (
            set(self._depfiles_tree.keys()).intersection(relevant_deps)
        )
        json_tree = {
            dep: convert_tree(self._depfiles_tree.get(dep))
            for dep in filtered_deps
        }
        if fpath:
            json.dump(json_tree, open(fpath, "w"), indent=4)
            return
        return json.dumps(json_tree, indent=4)

    def show_depfiles_tree(self, filters: DepType = DepType.ALL) -> None:
        """Show dependency and files"""
        self._gen_depfiles_tree()
        relevant_deps = (
            self._get_filtered_deps(filters) if filters else set()
        )
        def showfiles(branch: dict, indent=0):
            paths = branch.get("files", [])
            tree_prefix = self._tree_prefix(indent)
            for path in paths:
                print(f"{tree_prefix} {path.name}")

            dirs = {k:v for k,v in branch.items() if isinstance(v, dict)}
            for _dir, val in dirs.items():
                print(self._vertical_spacer(indent))
                self._print(f"{tree_prefix} [blue]{_dir}[/blue]/")
                showfiles(val, indent + 4)

        filtered_deps = (
            set(self._depfiles_tree.keys()).intersection(relevant_deps)
        )
        for dep in filtered_deps:
            deptree = self._depfiles_tree.get(dep)
            self._print(f"[bold cyan]{dep}[/bold cyan]")
            showfiles(deptree)
            print("\n")

    def dep_files(self, **kwargs) -> None:
        """Function for dep-files command"""
        fpath = kwargs.get("fpath")
        filters = kwargs.get("filters")
        if fpath is not None:
            self.depfiles_tree_json(fpath=fpath, filters=filters)
            return
        self.show_depfiles_tree(filters=filters)

    def get_unused_imports_tree(
        self, filters: DepType = DepType.ALL
    ) -> dict:
        """Get the file-unused imports tree"""
        self._gen_unused_import_tree()
        return self._unused_import_tree

    def show_unused_imports_tree(self) -> None:
        """Show file and unused imports tree"""
        self._gen_unused_import_tree()
        def showdep(branch: dict, indent=0):
            path_deps = branch.get("files", [])
            tree_prefix = self._tree_prefix(indent)
            maxwidth = (
                max(len(path.name) for path, _ in path_deps) if path_deps else 0
            )
            for path, deps in path_deps:
                deps = ", ".join(sorted(deps))
                deps = f" → [bold cyan]{deps}[/bold cyan]" if deps else ""
                self._print(f"{tree_prefix} {path.name:<{maxwidth}}{deps}")

            dirs = {k:v for k,v in branch.items() if isinstance(v, dict)}
            for _dir, val in dirs.items():
                print(self._vertical_spacer(indent))
                self._print(f"{tree_prefix} [blue]{_dir}[/blue]/")
                showdep(val, indent + 4)

        self._print(f"[bold magenta]Root ({self._root})[/bold magenta]")
        showdep(self._unused_import_tree)

    def unused_imports_tree_json(self, fpath: str) -> str | None:
        """Dump unused imports tree to json"""
        self._gen_unused_import_tree()
        json_tree = {}

        def copytree(src_branch: dict, dst_branch: dict):
            path_deps = src_branch.get("files", [])
            dst_branch["files"] = {}
            for path, deps in path_deps:
                dst_branch["files"][path.name] = sorted(deps)

            dirs = {k:v for k,v in src_branch.items() if isinstance(v, dict)}
            for _dir, val in dirs.items():
                dst_branch[_dir] = {}
                copytree(val, dst_branch[_dir])

        copytree(self._unused_import_tree, json_tree)
        if fpath:
            json.dump(json_tree, open(fpath, "w"), indent=4)
            return
        return json.dumps(json_tree, ident=4)

    def show_unused_imports(self) -> None:
        """Show all unused imports"""
        for dep in self._unused_deps:
            print(dep)

    def unused_imports_json(self, fpath: str) -> None:
        """Dump unused imports to json"""
        json_deps = {"unused_imports": sorted(self._unused_deps)}
        if fpath:
            json.dump(json_deps, open(fpath, "w"), indent=4)
        return json.dumps(json_deps, indent=4)

    def find_dep_instances(
        self, dependency: str
    ) -> dict[Path, list[Dependency]]:
        """Find files with instances of a dependency"""
        dep_instances = {}
        for path, deps in self._path_dependency_map.items():
            relevant_deps = [
                dep for dep in deps 
                if re.search(rf"\b{dependency}\b", dep.module)
            ]
            if relevant_deps:
                dep_instances[path] = relevant_deps
        return dep_instances

    def _get_file_lines(self, path: str, lines: list[int]) -> dict[int, str]:
        """Get specific lines from a file"""
        if not path.is_absolute():
            path = self._root / path
        lines = path.read_text(encoding="utf-8").splitlines()
        lineno_line_map = {lineno: lines[lineno - 1] for lineno in lines}
        return lineno_line_map

    def show_files_with_dep(self, dependency: str) -> None:
        """Show found dep in files"""
        dep_instances = self.find_dep_instances(dependency)
        instance_count = len([
            dep for deps in dep_instances.values() for dep in deps
        ])
        text = Text("\nDependency: ")
        text.append(dependency, style="bold cyan")
        text.append(f" ({instance_count} instances)\n")
        self._print(text)
        paths = [str(path) for path in dep_instances.keys()]
        paths = "\n".join(paths)
        print(paths)

    def files_with_dep_json(self, fpath: str, dependency: str) -> str | None:
        """Dump files with dep to json"""
        dep_instances = self.find_dep_instances(dependency)
        json_output = {"dependency": dependency}
        json_output["files"] = [str(path) for path in dep_instances.keys()]
        if fpath:
            json.dump(json_output, open(fpath, "w"), indent=4)
            return
        return json.dumps(json_output, ident=4)

    def _gen_files_with_dep_tree(self, dependency: str) -> None:
        """Generate file tree with dep"""
        dep_instances = self.find_dep_instances(dependency)
        self._files_with_dep_tree = {"files": []}
        for path, deps in dep_instances.items():
            dirparts = path.parent.parts
            branch = self._files_with_dep_tree
            for part in dirparts:
                branch = branch.setdefault(part, {"files": []})
            branch["files"].append((path, deps))

    def show_files_with_dep_tree(
        self,
        dependency: str,
        showlines: bool = False
    ) -> None:
        """Show files with dep as tree"""
        self._gen_files_with_dep_tree(dependency)

        def showdep(branch: dict, indent=0):
            path_deps = branch.get("files", [])
            tree_prefix = self._tree_prefix(indent)
            maxwidth = (
                max(len(path.name) for path, _ in path_deps) 
                if path_deps else 0
            )
            for path, deps in path_deps:
                print(f"{tree_prefix} {path.name}")
                if showlines:
                    fpath = str((self._root / path))
                    line_prefix = self._tree_prefix(indent + 4)
                    for dep in deps:
                        line = getline(fpath, dep.lineno).strip("\n")
                        print(f"{line_prefix} Line {dep.lineno:<5}: {line}")
                    print(self._vertical_spacer(indent + 4))

            dirs = {k:v for k,v in branch.items() if isinstance(v, dict)}
            for _dir, val in dirs.items():
                print(self._vertical_spacer(indent))
                self._print(f"{tree_prefix} [blue]{_dir}[/blue]/")
                showdep(val, indent + 4)

        self._print(f"Dependency: [bold cyan]{dependency}[/bold cyan]")
        showdep(self._files_with_dep_tree)

    def files_with_dep_tree_json(
        self,
        fpath: str,
        dependency: str,
        showlines: bool = False
    ) -> None:
        """Dump files with dep tree to json"""
        self._gen_files_with_dep_tree(dependency)
        json_tree = {}

        def copytree(src_branch: dict, dst_branch: dict):
            path_deps = src_branch.get("files", [])
            dst_branch["files"] = {} if showlines else []
            if showlines:
                for path, deps in path_deps:
                    dst_branch["files"][path.name] = {}
                    fpath = str((self._root / path))
                    for dep in deps:
                        line = getline(fpath, dep.lineno).strip("\n")
                        dst_branch["files"][path.name][dep.lineno] = line
            else:
                dst_branch["files"] = [path.name for path, _ in path_deps]

            dirs = {k:v for k,v in src_branch.items() if isinstance(v, dict)}
            for _dir, val in dirs.items():
                dst_branch[_dir] = {}
                copytree(val, dst_branch[_dir])

        copytree(self._files_with_dep_tree, json_tree)
        if fpath:
            json.dump(json_tree, open(fpath, "w"), indent=4)
            return
        return json.dumps(json_tree, ident=4)

    def show_stats(self, topn: int = 5) -> None:
        """Shows dependency stats"""
        print("\nDependency Statistics")
        print("-" * 50, end="\n\n")
        print(f"{'Files Scanned':<25}: {self._stats.files}\n")
        print(f"{'Imported Names':<25}: {self._stats.imported_names}")
        print(f"{'Import Statements':<25}: {self._stats.import_statements}")
        print(
            (
                f"{'Used Imports':<25}: "
                f"{self._stats.used_imports:<5} import occurances"
            )
        )
        print(
            (
                f"{'Unused Imports':<25}: "
                f"{self._stats.unused_imports:<5} import occurances\n"
            )
        )
        print(f"{'Unique Dependencies':<25}: {self._stats.unique_deps}\n")
        print("Dependency Types")
        print("-" * 50, end="\n\n")
        print(f"{'Standard library':<25}: {self._stats.stdlib}")
        print(f"{'Third-party':<25}: {self._stats.third_party}")
        print(f"{'Local':<25}: {self._stats.local}\n")
        print(f"Top {topn} Dependencies")
        print("-" * 50, end="\n\n")
        top_deps = "\n".join([
            f"{dep:<25}{count}"
            for dep, count 
            in self._stats.get_top_deps(topn)
        ])
        print(top_deps)


if __name__ == "__main__":
    pass

    




        





"""
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.

Core dependency analyzer
"""

import ast
from visitors import DependencyVisitor
from utils import walkpath
from pathlib import Path
import os
from rich.console import Console


class DepAnalyzer:

    def __init__(self) -> None:
        self._path: Path = None
        self._packages: set[str] = set()
        self._ignorelist: set[str] = set()
        self._path_dep_map: dict[str, set[str]] = {}
        self._dep_path_map: dict[str, list[str]] = {}
        self._root: str = ""
        self.filedep_tree = {"files": []}
        self._console = Console()

    def ignore(self, ignorelist: list[str]) -> None:
        """Adds files/directories to ignorelist"""
        self._ignorelist.set(ignorelist)
        self._ignorelist = set(ignorelist)

    def _get_file_deps(self, fpath: str) -> list[str]:
        """Get dependencies in a file"""
        with open(fpath, "r", encoding="utf-8") as fh:
            source = fh.read()
            tree = ast.parse(source)
            visitor = DependencyVisitor()
            visitor.visit(tree)
            return visitor.packages

    def _get_relative_path(self, path: str):
        path = Path(path)
        return path.relative_to(self._root)

    def scan(self, root: str = ".") -> None:
        """Scans a python file(s) in a directory/sub-directory"""
        self._root = Path(root)
        for path in walkpath(root, self._ignorelist):
            packages = self._get_file_deps(path)
            packages = set(packages)
            self._path_dep_map[path] = packages
            for pkg in packages:
                self._dep_path_map.setdefault(pkg, []).append(path)
            self._packages.update(packages)
        self._gen_filedeps_tree()
        self._gen_depfiles_tree()

    @property
    def packages(self):
        return self._packages

    def show_packages(self):
        print("\n".join(self._packages))

    def _tree_prefix(self, indent: int = 0) -> str:
        """Generates tree prefix with indentation"""
        spaces = " " * indent
        #return f"{spaces}|__"
        return f"{spaces}├──"

    def _vertical_spacer(self, indent: int = 0) -> str:
        """Generates a vertical spacer"""
        spaces = " " * indent
        return f"{spaces}|"

    #def show_filedeps(self) -> str:
    #    """Shows file and dependencies"""
    #    grouped_dirs_and_deps = {}
    #    for path, deps in self._path_dep_map.items():
    #        dirname = os.path.dirname(path)
    #        basename = os.path.basename(path)
    #        grouped_dirs_and_deps.setdefault(
    #            dirname, []
    #        ).append((basename, deps))

    #    print(f"Root ({self._root})")
    #    for dirname, deplist in grouped_dirs_and_deps.items():
    #        indent = 0
    #        print(self._vertical_spacer())
    #        relpath = Path(dirname).relative_to(self._root)
    #        parts = relpath.parts
    #        if parts:
    #            for part in parts:
    #                tree_prefix = self._tree_prefix(indent)
    #                print(f"{tree_prefix} {part}/")
    #                indent += 4

    #        max_filewitdh = max(len(file) for file, _ in deplist)
    #        for file, deps in deplist:
    #            deps = sorted(deps) if deps else ""
    #            deps = str(deps)[1:-1].replace("'", "")
    #            deps = f" -> {deps}" if deps else ""
    #            tree_prefix = self._tree_prefix(indent)
    #            print(f"{tree_prefix} {file:<{max_filewitdh}} {deps}")

    def _print(self, text: str) -> None:
        """Coloured print"""
        self._console.print(text)

    def _gen_filedeps_tree(self) -> None:
        """Generate file dependency tree"""
        self.filedep_tree = {"files": []}
        for path, deps in self._path_dep_map.items():
            dirname = os.path.dirname(path)
            basename = os.path.basename(path)
            relpath = Path(dirname).relative_to(self._root)
            dirparts = relpath.parts
            branch = self.filedep_tree
            for part in dirparts:
                branch = branch.setdefault(part, {"files": []})
            branch["files"].append((basename, deps))

    def _gen_depfiles_tree(self) -> None:
        """Generate dependency file tree"""
        self._depfile_tree = {}
        for path, deps in self._path_dep_map.items():
            dirname = os.path.dirname(path)
            basename = os.path.basename(path)
            relpath = Path(dirname).relative_to(self._root)
            dirparts = relpath.parts
            for dep in deps:
                branch = self._depfile_tree.setdefault(dep, {"files": []})
                for part in dirparts:
                    branch = branch.setdefault(part, {"files": []})
                branch["files"].append(basename)

    def show_filedeps(self):
        """Show file and dependencies"""
        def showdep(branch: dict, indent=0):
            files = branch.get("files", [])
            tree_prefix = self._tree_prefix(indent)
            max_filewitdh = (
                max(len(file) for file, _ in files) if files else 0
            )
            for file, deps in files:
                deps = sorted(deps) if deps else ""
                deps = str(deps)[1:-1].replace("'", "")
                deps = f" → [bold cyan]{deps}[/bold cyan]" if deps else ""
                self._print(f"{tree_prefix} {file:<{max_filewitdh}}{deps}")

            dirs = {k:v for k,v in branch.items() if isinstance(v, dict)}
            for _dir, val in dirs.items():
                print(self._vertical_spacer(indent))
                self._print(f"{tree_prefix} [blue]{_dir}[/blue]/")
                showdep(val, indent + 4)

        self._print(f"[bold magenta]Root ({self._root})[/bold magenta]")
        showdep(self.filedep_tree)

    def show_depfiles(self):
        """Show dependency and files"""
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

        for dep, tree in self._depfile_tree.items():
            self._print(f"[bold cyan]{dep}[/bold cyan]")
            showfiles(tree)
            print("\n")

    #def show_depfiles(self) -> str:
    #    def dirparts(path):
    #        dirname = os.path.dirname(path)


    #    for package, paths in self._dep_path_map.items():
    #        print(f"{package} ({len(paths)} files)")
    #        #fmtstr = (" " * 5) + "|" + ("_" * 5)
    #        tree_prefix = self._tree_prefix()
    #        sorted_paths = [
    #            Path(path).relative_to(self._root)
    #            for path in paths
    #        ]
    #        #sorted_paths.sort(key=lamdba p: len(p.parts))
    #        for path in sorted_paths:
    #            dirparts(path)

    #            #path = Path(path).relative_to(self._root)
    #            print(f"{tree_prefix} {path}")
    #        print("\n")





if __name__ == "__main__":
    dp = DepAnalyzer()
    dp.scan(r"C:\users\shine\pyprojs\insta-likecom-bot\modules")
    from pprint import pprint
    #pprint(dp.packages, width=120)
    #dp.show_depmap()
    #dp.show_filedeps()
    #dp.create_filedeps()
    #dp.show_filedeps1()
    #dp.show_depfiles()
    #dp.show_depfiles()
    dp.show_filedeps()
    #dp.show_packages()

    




        





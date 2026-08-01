"""
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.

AST Visitors for dependency analysis
"""

import ast
from dataclasses import dataclass
from typing import TypeAlias


@dataclass
class Dependency:
    module: str
    level: int
    lineno: int
    alias: str = ""


@dataclass
class ImportItem:
    imported: str
    lineno: int
    module: str | None = None
    asname: str | None = None

    @property
    def bound_name(self):
        return self.asname or self.imported


ImportName: TypeAlias = str


class DependencyVisitor(ast.NodeVisitor):

    def __init__(self):
        self._deps: list[Dependency] = []
        self._import_name_map: dict[ImportName, list[ImportItem]] = {}
        self._used_importnames: set[ImportName] = set()

    @property
    def deps(self):
        return self._deps

    @property
    def imports(self):
        return self._import_name_map

    @property
    def used_imports(self):
        return set(self._used_importnames)

    @property
    def unused_imports(self):
        imported_names = set(self._import_name_map.keys())
        unused_names = imported_names.difference(self._used_importnames)
        return unused_names

    def _get_toplevel_module(self, name: str) -> str:
        """Get the top level module"""
        return name.split(".", 1)[0] if name else ""

    def _update_imported_names(self, node) -> None:
        """Updates imported names"""
        if not hasattr(node, "names"):
            return

        for alias in node.names:
            importkey = alias.asname or alias.name
            self._import_name_map.setdefault(
                importkey, []
            ).append(
                ImportItem(
                    imported=alias.name,
                    asname=alias.asname,
                    module=getattr(node, "module", alias.name),
                    lineno=alias.lineno
                )
            )

    def _get_attr_namepath(self, node: ast.Attribute):
        """Get namepath from Attribute"""
        if not isinstance(node, (ast.Name, ast.Attribute)):
            return ""
        if isinstance(node, ast.Name):
            return node.id
        return (
            f"{self._get_attr_namepath(node.value)}."
            f"{node.attr}"
        )

    def _get_matching_importname(self, namepath: str) -> str:
        """Get matching import name from import mapping"""
        parts = namepath.split(".")
        while parts:
            name = ".".join(parts)
            if name in self._import_name_map:
                return name
            parts = parts[:-1]
        return ""

    def visit_Import(self, node):
        self._update_imported_names(node)
        self._deps.extend([
            Dependency(
                module=self._get_toplevel_module(alias.name),
                level=0,
                lineno=node.lineno,
                alias=alias.asname
            )
            for alias in node.names
        ])
        
    def visit_ImportFrom(self, node):
        level = node.level
        self._update_imported_names(node)
        if node.module:
            module = self._get_toplevel_module(node.module)
            self._deps.append(
                Dependency(
                    module=module,
                    level=level,
                    lineno=node.lineno,
                    alias=None
                )
            )
        else:
            self._deps.extend([
                Dependency(
                    module=self._get_toplevel_module(alias.name),
                    level=0,
                    lineno=node.lineno,
                    alias=alias.asname
                )
                for alias in node.names
            ])

    def visit_Name(self, node):
        if (
            isinstance(node.ctx, ast.Load) 
            and node.id in self._import_name_map
        ):
            self._used_importnames.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        namepath = self._get_attr_namepath(node)
        import_name = self._get_matching_importname(namepath)
        if not import_name:
            self.generic_visit(node)
        else:
            self._used_importnames.add(import_name)
        

if __name__ == "__main__":
    pass



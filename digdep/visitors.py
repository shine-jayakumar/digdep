"""
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.

AST Visitors for dependency analysis
"""

import ast


class DependencyVisitor(ast.NodeVisitor):

    def __init__(self):
        self._deps: list[tuple[str, int]] = []

    @property
    def deps(self):
        return self._deps

    def _get_toplevel_module(self, name: str) -> str:
        """Get the top level module"""
        return name.split(".", 1)[0] if name else ""

    def visit_Import(self, node):
        self._deps.extend([
            (self._get_toplevel_module(alias.name), 0)
            for alias in node.names
        ])
        
    def visit_ImportFrom(self, node):
        level = node.level
        if node.module:
            module = self._get_toplevel_module(node.module)
            self._deps.append((module, level))
        else:
            for alias in node.names:
                module = self._get_toplevel_module(alias.name)
                self._deps.append((module, level))



if __name__ == "__main__":
    pass



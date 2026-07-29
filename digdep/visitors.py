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
        self._deps = []

    @property
    def deps(self):
        return self._deps

    def visit_Import(self, node):
        self._deps.extend([
            alias.name.split(".", 1)[0] for alias in node.names
        ])
        
    def visit_ImportFrom(self, node):
        if node.level == 0:
            self._deps.append(node.module.split(".")[0])


if __name__ == "__main__":
    pass



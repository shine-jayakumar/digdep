"""
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.

Utility methods
"""

from pathlib import Path
from collections.abc import Iterator


def walkpath(root: str | Path, ignorelist: set[str]) -> Iterator[Path]:
    """Get .py files from directories and sub-directories"""
    if not isinstance(root, Path):
        root = Path(root)
    if not root.exists():
        raise Exception("File/Directory doesn't exist")

    if root.is_file():
        return root

    for path in root.iterdir():
        if path.name in ignorelist:
            continue
        if path.is_dir():
            yield from walkpath(path, ignorelist)

        elif path.suffix == ".py":
            yield path


if __name__ == "__main__":
    pass


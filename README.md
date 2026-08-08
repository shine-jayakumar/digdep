# DigDep

![Version](https://img.shields.io/static/v1?label=version&message=v0.1.1&color=blue)
[![PyPI version](https://img.shields.io/pypi/v/digdep.svg)](https://pypi.org/project/digdep/)
[![Python versions](https://img.shields.io/pypi/pyversions/digdep.svg)](https://pypi.org/project/digdep/)
![License](https://img.shields.io/static/v1?label=license&message=MIT&color=green)
![Status](https://img.shields.io/badge/status-alpha-yellow.svg)
![Open Source](https://img.shields.io/static/v1?label=OpenSource&message=Yes&color=brightgreen)

A lightweight Python dependency analyzer that scans Python projects and visualizes import relationships.

---

## Features

- Scan Python projects for imported modules
- List project dependencies
- Generate **File → Dependency** trees
- Generate **Dependency → File** trees
- Detect unused imports
- Find files that import a specific dependency
- Show exact import lines for a dependency
- Filter dependencies by type:
  - Standard Library
  - Third-party
  - Local
- Ignore files and directories during analysis
- Read ignore patterns from a file
- Export analysis results as JSON
- Use from the command line or as a Python library
- Support ASCII output for environments where Unicode tree characters are unavailable

---

## Installation

```bash
pip install digdep
```

---
# Quick Start

## Command Line

List project dependencies:

```bash
digdep deps ./myproject
```

Show the File → Dependency tree:

```bash
digdep deps ./myproject --tree
```

Show the Dependency → File tree:

```bash
digdep deps ./myproject --tree --reverse
```

Show unused imports:

```bash
digdep deps ./myproject --unused
```

Show unused imports as a tree:

```bash
digdep deps ./myproject --unused --tree
```

Find files importing a dependency:

```bash
digdep find-dep requests ./myproject
```

Show the dependency as a file tree:

```bash
digdep find-dep requests ./myproject --tree
```

Show the exact import lines:

```bash
digdep find-dep requests ./myproject --tree --showlines
```

Export results as JSON:

```bash
digdep deps ./myproject --tree -o file_tree.json
```


For the complete CLI reference, see:

**📖 [CLI Documentation](https://github.com/shine-jayakumar/digdep/blob/master/docs/CLI.md)**

---

## DigDep Library

```python
from digdep import DepAnalyzer

analyzer = DepAnalyzer()
analyzer.analyze("./myproject")

analyzer.show_deps()
```

For the complete Python API guide, see:

**📖 [DigDep Library Documentation](https://github.com/shine-jayakumar/digdep/blob/master/docs/API.md)**

---

## Example Output

### File → Dependency Tree

```text
Root (/projects/example)

├── main.py              → requests, pathlib
├── config.py            → json
│
├── modules/
│   ├── logger.py        → logging
│   ├── parser.py        → re, typing
│
└── utils/
    └── helpers.py       → functools
```

### Find Dependency
```text
Dependency: ctypes
├── accessibleinfo.py
    ├── Line 1    : from ctypes import c_float
    ├── Line 2    : from ctypes import c_int
    ├── Line 3    : from ctypes import c_wchar
    ├── Line 4    : from ctypes import c_bool
    ├── Line 5    : from ctypes import Structure
    ├── Line 6    : from ctypes.wintypes import BOOL
    ├── Line 7    : from ctypes.wintypes import WCHAR
    │
├── jabdriver.py
    ├── Line 5    : from ctypes import byref
    ├── Line 6    : from ctypes import CDLL
    ├── Line 7    : from ctypes import c_long
    ├── Line 8    : from ctypes.wintypes import HWND
    │
```

---

## Documentation

| Guide | Description |
|-------|-------------|
| **README** | Installation and quick start |
| **docs/cli.md** | Complete command-line reference |
| **docs/api.md** | DigDep library guide |

---

## Roadmap

- Circular dependency detection
- Multiple output formats
- Performance improvements

---

## Requirements

- Python 3.11+

---

## License

Released under the MIT License.

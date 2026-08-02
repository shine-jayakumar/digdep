# DigDep

![Version](https://img.shields.io/static/v1?label=version&message=v0.1.0&color=blue)
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
- Filter dependencies by type (Standard Library, Third-party, Local)
- Export results as JSON
- Use from the command line or as a Python library

---

## Installation

```bash
pip install digdep
```

---

# Quick Start

## Command Line

List project dependencies.

```bash
digdep deps ./myproject
```

Show the File → Dependency tree.

```bash
digdep file-tree ./myproject
```

Show the Dependency → File tree.

```bash
digdep dep-tree ./myproject
```

Show unused imports.

```bash
digdep unused-imports ./myproject
```

For the complete CLI reference, see:

**📖 [CLI Documentation](https://github.com/shine-jayakumar/digdep/blob/master/docs/CLI.md)**

---

## Python Library

```python
from digdep import DepAnalyzer

analyzer = DepAnalyzer()
analyzer.analyze("./myproject")

analyzer.show_deps()
```

For the complete Python API guide, see:

**📖 [Python Library Documentation](https://github.com/shine-jayakumar/digdep/blob/master/docs/API.md)**

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

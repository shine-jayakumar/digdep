# DigDep

![Version](https://img.shields.io/static/v1?label=version&message=v.0.0.5&color=blue)
![License](https://img.shields.io/static/v1?label=license&message=MIT&color=green)
![Status](https://img.shields.io/badge/status-alpha-yellow.svg)
![Open Source](https://img.shields.io/static/v1?label=OpenSource&message=Yes&color=brightgreen)
![GitHub issues](https://img.shields.io/github/issues/shine-jayakumar/docdsl)
![Last Commit](https://img.shields.io/github/last-commit/shine-jayakumar/docdsl)

A lightweight Python dependency analyzer that scans Python projects and visualizes import relationships.

---

## Installation

```bash
pip install digdep
```
---

## Quick Start (CLI)

List all imported packages:

```bash
digdep packages ./myproject
```

Show the File → Dependency tree:

```bash
digdep file-tree ./myproject
```

Show the Dependency → File tree:

```bash
digdep dep-tree ./myproject
```

---

## Sample Output

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

### Dependency → File Tree

```text
requests
├── main.py

re
├── modules/
│   └── parser.py

logging
├── modules/
│   └── logger.py
```

---

## Filtering

Filter dependencies by type.

Show only standard library imports:

```bash
digdep file-tree ./myproject --type stdlib
```

Show both standard library and third-party imports:

```bash
digdep file-tree ./myproject --type stdlib,third-party
```

Show only local imports:

```bash
digdep file-tree ./myproject --type local
```

---

## Ignoring Directories

### Ignore from command line

```bash
digdep file-tree ./myproject --ignore venv __pycache__ tests
```

### Ignore from a file

Create a text file (for example, `ignore.txt`):

```text
venv
.git
build
__pycache__
tests
```

Then run:

```bash
digdep . --ignore-file ignore.txt
```

Each non-empty line in the file is treated as a directory to ignore.

The `--ignore` and `--ignore-file` options can be used together.

---

## Write Output to a File

Use the `-o` (`--output`) option to write command output to a file. Currently, DigDep supports JSON output.

### Export the dependency list

```bash
digdep deps . -o deps.json
```

Output:

```json
{
    "dependencies": [
        "argparse",
        "ast",
        "json",
        "pathlib",
        "rich"
    ]
}
```

### Export the file-dependency tree

```bash
digdep file-tree . -o file-tree.json
```

### Export the dependency-file tree

```bash
digdep dep-tree . -o dep-tree.json
```

The output format is determined by the file extension. Currently, only `.json` is supported.


## Redirecting Output

Save the generated tree to a file:

```bash
digdep dep-tree ./myproject > dependencies.txt
```

---

## Commands

| Command | Description |
|---------|-------------|
| `packages` | List all imported packages |
| `file-tree` | Show the File → Dependency tree |
| `dep-tree` | Show the Dependency → File tree |

Run `digdep <command> --help` for command-specific options.

---

## Using as a Python Library

```python
from digdep import DepAnalyzer, DepType

analyzer = DepAnalyzer()

# Ignoring directories
analyzer.ignore([
    "__pycache__",
    "venv",
    "build",
    "tests"
])

analyzer.scan("./myproject")

# List imported packages
packages = analyzer.get_packages()

# Get the File -> Dependency tree
filedep_tree = analyzer.get_filedep_tree()

# Get the Dependency -> File tree
depfile_tree = analyzer.get_depfile_tree()

```

Filter dependencies by type:

```python
from digdep import DepAnalyzer, DepType

analyzer = DepAnalyzer()
analyzer.scan("./myproject")

# Show only standard library imports
filedep_tree = analyzer.get_filedep_tree(
    filters=DepType.STDLIB
)

# Show standard library and third-party imports
depfile_tree = analyzer.get_depfile_tree(
    filters=DepType.STDLIB | DepType.THIRD_PARTY
)
```

---
## Roadmap

- Local module detection
- Dependency statistics
- JSON export
- Circular dependency detection
- Unused dependency detection

---

## Requirements

- Python 3.11+

---

## License

Released under the MIT License.

---

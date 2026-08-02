# DigDep Library

The `digdep` library provides a Python API for analyzing import dependencies in Python projects. It can be used to inspect project dependencies, generate dependency trees, detect unused imports, and collect dependency statistics.

---

# Installation

```bash
pip install digdep
```

---

# Quick Start

```python
from digdep import DepAnalyzer

analyzer = DepAnalyzer()
analyzer.analyze("./myproject")

analyzer.show_deps()
```

---

# Basic Usage

## Analyze a Project

```python
from digdep import DepAnalyzer

analyzer = DepAnalyzer()
analyzer.analyze("./myproject")
```

---

## Ignore Directories

```python
analyzer.ignore([
    "venv",
    "__pycache__",
    "tests"
])

analyzer.analyze("./myproject")
```

---

## Ignore Directories from a File

```python
analyzer.ignore_from_file(".digdepignore")
analyzer.analyze("./myproject")
```

Example `.digdepignore`

```text
venv
__pycache__
tests
build
dist
```

---

# Dependency Types

Dependencies can be filtered using the `DepType` enum.

```python
from digdep import DepType

DepType.STDLIB
DepType.THIRD_PARTY
DepType.LOCAL
DepType.ALL
```

Example

```python
analyzer.show_deps(DepType.THIRD_PARTY)
```

---

# Listing Dependencies

Return the dependencies as a tuple.

```python
deps = analyzer.get_deps()

print(deps)
```

Display them directly.

```python
analyzer.show_deps()
```

Export as JSON.

```python
json_text = analyzer.deps_json(None)
```

Write JSON to a file.

```python
analyzer.deps_json("dependencies.json")
```

---

# File Dependency Tree

Generate a tree mapping files to their imported dependencies.

Retrieve the tree.

```python
tree = analyzer.get_file_tree()
```

Display the tree.

```python
analyzer.show_file_tree()
```

Export to JSON.

```python
analyzer.file_tree_json("file_tree.json")
```

---

# Dependency Tree

Generate a tree mapping dependencies to the files that import them.

Retrieve the tree.

```python
tree = analyzer.get_dep_tree()
```

Display the tree.

```python
analyzer.show_dep_tree()
```

Export to JSON.

```python
analyzer.dep_tree_json("dependency_tree.json")
```

---

# Unused Imports

Retrieve the unused import tree.

```python
tree = analyzer.get_unused_imports_tree()
```

Display unused imports.

```python
analyzer.show_unused_imports()
```

---

# Dependency Statistics

Display project statistics.

```python
analyzer.show_stats()
```

Statistics include:

- Files scanned
- Imported items
- Import statements
- Used imports
- Unused imports
- Unique dependencies
- Standard library dependencies
- Third-party dependencies
- Local dependencies
- Top imported modules

---

# Accessing Statistics

Statistics are also available programmatically.

```python
stats = analyzer.stats

print(stats.files)
print(stats.unique_deps)
print(stats.third_party)
```

---

# ASCII Tree Mode

Use ASCII characters instead of Unicode tree characters.

```python
analyzer = DepAnalyzer(is_ascii=True)
```

---

# Typical Workflow

```python
from digdep import DepAnalyzer

analyzer = DepAnalyzer()

analyzer.ignore([
    "venv",
    "__pycache__",
])

analyzer.analyze("./project")

analyzer.show_deps()

analyzer.show_file_tree()

analyzer.show_dep_tree()

analyzer.show_unused_imports()

analyzer.show_stats()
```

---

# Public API

## Classes

| Class | Description |
|--------|-------------|
| `DepAnalyzer` | Main dependency analyzer. |
| `DepType` | Dependency type filter. |
| `Stats` | Statistics collected during analysis. |

---

## DepAnalyzer Methods

| Method | Description |
|---------|-------------|
| `analyze(path)` | Analyze a project. |
| `ignore(list)` | Ignore files or directories. |
| `ignore_from_file(path)` | Read ignored paths from a file. |
| `get_deps()` | Return detected dependencies. |
| `show_deps()` | Print detected dependencies. |
| `deps_json()` | Export dependencies as JSON. |
| `get_file_tree()` | Return the file → dependency tree. |
| `show_file_tree()` | Print the file → dependency tree. |
| `file_tree_json()` | Export the file tree as JSON. |
| `get_dep_tree()` | Return the dependency → file tree. |
| `show_dep_tree()` | Print the dependency tree. |
| `dep_tree_json()` | Export the dependency tree as JSON. |
| `get_unused_imports_tree()` | Return unused imports. |
| `show_unused_imports()` | Print unused imports. |
| `show_stats()` | Display dependency statistics. |

---

## Properties

| Property | Description |
|----------|-------------|
| `stats` | Statistics from the last analysis. |
| `ignorelist` | Current ignore list. |

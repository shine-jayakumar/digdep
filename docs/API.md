# DigDep Library

The `digdep` library provides a Python API for analyzing import dependencies in Python projects. It can be used to inspect project dependencies, generate dependency trees, find files importing a dependency, detect unused imports, and collect dependency statistics.

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

Example `.digdepignore`:

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

Example:

```python
analyzer.show_deps(filters=DepType.THIRD_PARTY)
```

Multiple dependency types can be combined:

```python
filters = DepType.STDLIB | DepType.LOCAL

analyzer.show_deps(filters=filters)
```

---

# Listing Dependencies

Return the dependencies as a tuple:

```python
deps = analyzer.get_deps()

print(deps)
```

Display them directly:

```python
analyzer.show_deps()
```

Export as JSON:

```python
json_text = analyzer.deps_json(None)
```

Write JSON to a file:

```python
analyzer.deps_json("dependencies.json")
```

Dependency filters can also be supplied when displaying or exporting dependencies:

```python
analyzer.show_deps(filters=DepType.THIRD_PARTY)

analyzer.deps_json(
    "dependencies.json",
    filters=DepType.THIRD_PARTY
)
```

---

# File → Dependency Tree

Generate a tree mapping files to their imported dependencies.

Retrieve the tree:

```python
tree = analyzer.get_filedep_tree()
```

Display the tree:

```python
analyzer.show_filedep_tree()
```

Export the tree as JSON:

```python
analyzer.filedep_tree_json("file_tree.json")
```

Dependency types can be filtered:

```python
analyzer.show_filedep_tree(
    filters=DepType.THIRD_PARTY
)
```

The same filter can be used when exporting the tree:

```python
analyzer.filedep_tree_json(
    "file_tree.json",
    filters=DepType.THIRD_PARTY
)
```

---

# Dependency → File Tree

Generate a tree mapping dependencies to the files that import them.

Retrieve the tree:

```python
tree = analyzer.get_depfiles_tree()
```

Display the tree:

```python
analyzer.show_depfiles_tree()
```

Export the tree as JSON:

```python
analyzer.depfiles_tree_json("dependency_tree.json")
```

Dependency types can be filtered:

```python
analyzer.show_depfiles_tree(
    filters=DepType.THIRD_PARTY
)
```

---

# Unused Imports

Retrieve the unused import tree:

```python
tree = analyzer.get_unused_imports_tree()
```

Display all unused imports:

```python
analyzer.show_unused_imports()
```

Export all unused imports as JSON:

```python
json_text = analyzer.unused_imports_json(None)
```

Write unused imports to a JSON file:

```python
analyzer.unused_imports_json("unused_imports.json")
```

The unused import tree can also be displayed:

```python
analyzer.show_unused_imports_tree()
```

Export the unused import tree as JSON:

```python
analyzer.unused_imports_tree_json("unused_imports_tree.json")
```

---

# Finding Files with a Dependency

The `find_dep_instances()` method finds occurrences of a dependency in the analyzed project.

```python
instances = analyzer.find_dep_instances("requests")
```

The returned value is a dictionary mapping project-relative paths to lists of `Dependency` objects:

```python
{
    Path("app/api.py"): [
        Dependency(
            module="requests",
            level=0,
            lineno=5,
            alias=""
        )
    ]
}
```

This provides access to the raw `Dependency` objects detected by the AST visitor.

For example:

```python
instances = analyzer.find_dep_instances("requests")

for path, dependencies in instances.items():
    print(path)

    for dependency in dependencies:
        print(dependency.module)
        print(dependency.lineno)
        print(dependency.alias)
```

---

# Display Files with a Dependency

Display files importing a particular dependency:

```python
analyzer.show_files_with_dep("requests")
```

The output includes the dependency and the number of matching instances.

---

# Export Files with a Dependency

Export the files containing a dependency as JSON:

```python
analyzer.files_with_dep_json(
    "requests.json",
    "requests"
)
```

The generated JSON contains the dependency and the files in which it occurs.

---

# File Tree for a Dependency

A dependency can also be displayed as a file tree.

```python
analyzer.show_files_with_dep_tree("requests")
```

The tree can optionally include the exact import lines:

```python
analyzer.show_files_with_dep_tree(
    "requests",
    showlines=True
)
```

For example, this can show information such as:

```text
Dependency: requests
├── api.py
│   Line 5    : import requests
└── services
    └── client.py
        Line 3    : import requests as req
```

---

# Export Dependency File Tree

The dependency file tree can be exported as JSON:

```python
analyzer.files_with_dep_tree_json(
    "requests.json",
    "requests"
)
```

Import lines can also be included:

```python
analyzer.files_with_dep_tree_json(
    "requests.json",
    "requests",
    showlines=True
)
```

When `showlines` is enabled, the JSON contains the matching line numbers and source lines.

---

# Dependency Statistics

Display project statistics:

```python
analyzer.show_stats()
```

The number of top dependencies displayed can be controlled with `topn`:

```python
analyzer.show_stats(topn=10)
```

Statistics include information such as:

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

Statistics are also available programmatically:

```python
stats = analyzer.stats

print(stats.files)
print(stats.unique_deps)
print(stats.third_party)
```

---

# ASCII Tree Mode

Use ASCII characters instead of Unicode tree characters:

```python
analyzer = DepAnalyzer(is_ascii=True)
```

This is useful when the terminal does not support Unicode tree characters.

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

# List dependencies
analyzer.show_deps()

# File → dependency tree
analyzer.show_filedep_tree()

# Dependency → file tree
analyzer.show_depfiles_tree()

# Unused imports
analyzer.show_unused_imports()

# Dependency statistics
analyzer.show_stats()

# Find files importing a dependency
analyzer.show_files_with_dep("requests")
```

---

## DepAnalyzer Methods

| Method | Description |
| --- | --- |
| `analyze(path)` | Analyze a project. |
| `ignore(list)` | Ignore files or directories. |
| `ignore_from_file(path)` | Read ignored paths from a file. |
| `get_deps()` | Return detected dependencies. |
| `show_deps()` | Print detected dependencies. |
| `deps_json()` | Export dependencies as JSON. |
| `get_filedep_tree()` | Return the file → dependency tree. |
| `show_filedep_tree()` | Print the file → dependency tree. |
| `filedep_tree_json()` | Export the file → dependency tree as JSON. |
| `get_depfiles_tree()` | Return the dependency → file tree. |
| `show_depfiles_tree()` | Print the dependency → file tree. |
| `depfiles_tree_json()` | Export the dependency → file tree as JSON. |
| `get_unused_imports_tree()` | Return the unused import tree. |
| `show_unused_imports()` | Print unused imports. |
| `unused_imports_json()` | Export unused imports as JSON. |
| `show_unused_imports_tree()` | Print the unused import tree. |
| `unused_imports_tree_json()` | Export the unused import tree as JSON. |
| `find_dep_instances(dependency)` | Return files containing instances of a dependency. |
| `show_files_with_dep(dependency)` | Display files containing a dependency. |
| `files_with_dep_json(fpath, dependency)` | Export files containing a dependency as JSON. |
| `show_files_with_dep_tree(dependency, showlines=False)` | Display files containing a dependency as a tree. |
| `files_with_dep_tree_json(fpath, dependency, showlines=False)` | Export the dependency file tree as JSON. |
| `show_stats(topn=5)` | Display dependency statistics. |

---


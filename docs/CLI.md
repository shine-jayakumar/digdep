# Command Line Interface (CLI)

`digdep` scans Python projects and inspects their import dependencies.

## Usage

```bash
digdep <command> <path> [OPTIONS]
```

- `<command>` — The action to perform.
- `<path>` — Path to the Python project to analyze.

---

## Commands

| Command | Description |
| ------- | ----------- |
| `deps` | List all detected dependencies. |
| `file-tree` | Display a file → dependency tree. |
| `dep-tree` | Display a dependency → file tree. |
| `unused-imports` | Display unused imports grouped by file. |
| `stats` | Display dependency statistics. |

---

## Common Options

The following options are available for all commands.

| Option | Description |
| ------ | ----------- |
| `-h`, `--help` | Show the help message and exit. |
| `-v`, `--version` | Show the installed version of **digdep** and exit. |
| `-i`, `--ignore NAME [NAME ...]` | Ignore one or more directories or files. |
| `-I`, `--ignore-file FILE` | Read directories or files to ignore from a file. |
| `-t`, `--type TYPES` | Filter dependency types. Accepted values are `stdlib`, `third-party`, `local`, or `all` (default). Multiple values can be supplied as a comma-separated list. |
| `-o`, `--output FILE` | Write the output to a file instead of the console. |

---

# Command Reference

## `deps`

List all detected dependencies.

### Examples

```bash
digdep deps ./myproject
```

Show only third-party dependencies.

```bash
digdep deps ./myproject --type third-party
```

Show standard library and local dependencies.

```bash
digdep deps ./myproject --type stdlib,local
```

---

## `file-tree`

Display the File → Dependency tree.

### Examples

```bash
digdep file-tree ./myproject
```

Ignore directories while scanning.

```bash
digdep file-tree ./myproject --ignore venv __pycache__ tests
```

Read ignored paths from a file.

```bash
digdep file-tree ./myproject --ignore-file .digdepignore
```

Write the output to a JSON file.

```bash
digdep file-tree ./myproject --output file_tree.json
```

or

```bash
digdep file-tree ./myproject -o file_tree.json
```

---

## `dep-tree`

Display the Dependency → File tree.

### Examples

```bash
digdep dep-tree ./myproject
```

Redirect the output using the shell.

```bash
digdep dep-tree ./myproject > dependencies.txt
```

---

## `unused-imports`

Display unused imports grouped by file.

### Examples

```bash
digdep unused-imports ./myproject
```

Show only unused standard library imports.

```bash
digdep unused-imports ./myproject --type stdlib
```

Show only unused local imports.

```bash
digdep unused-imports ./myproject --type local
```

---

## `stats`

Display dependency statistics for the project.

### Options

| Option | Description |
| ------ | ----------- |
| `-tn`, `--topn NUM` | Display the top **NUM** imported dependencies. Defaults to `5`. |

### Examples

Display project statistics.

```bash
digdep stats ./myproject
```

Display the top 10 imported dependencies.

```bash
digdep stats ./myproject --topn 10
```

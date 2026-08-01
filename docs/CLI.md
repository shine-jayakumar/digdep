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

## Examples

### List dependencies

```bash
digdep deps ./myproject
```

### Display the file dependency tree

```bash
digdep file-tree ./myproject
```

### Display the dependency tree

```bash
digdep dep-tree ./myproject
```

### Find unused imports

```bash
digdep unused-imports ./myproject
```

### Show dependency statistics

```bash
digdep stats ./myproject
```

### Ignore directories

```bash
digdep file-tree ./myproject --ignore venv __pycache__ tests
```

### Read ignored paths from a file

```bash
digdep deps ./myproject --ignore-file .digdepignore
```

### Filter dependency types

```bash
digdep deps ./myproject --type third-party
```

```bash
digdep deps ./myproject --type stdlib,local
```

### Save output to a file

```bash
digdep file-tree ./myproject --output file_tree.json
```

or

```bash
digdep file-tree ./myproject -o file_tree.json
```

### Redirect output using the shell

```bash
digdep dep-tree ./myproject > dependencies.txt
```

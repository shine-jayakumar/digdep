
# Command Line Interface (CLI)

`digdep` scans Python projects and inspects their import dependencies.

## Usage

```bash
digdep <command> <path> [OPTIONS]
```

- `<command>` — The action to perform.
- `<path>` — Path to the Python project to analyze.
- `[OPTIONS]` — Command-specific and common options.

---

## Commands

| Command | Description |
| --- | --- |
| `deps` | List dependencies and optionally display them as a tree, reverse tree, or unused imports. |
| `find-dep` | Find files that import a specified dependency. |
| `stats` | Display dependency statistics. |

---

# Common Options

The following options are available where supported by the command.

| Option | Description |
| --- | --- |
| `-h`, `--help` | Show the help message and exit. |
| `-v`, `--version` | Show the installed version of **digdep** and exit. |
| `-i`, `--ignore NAME [NAME ...]` | Ignore one or more directories or files. |
| `-I`, `--ignore-file FILE` | Read directories or files to ignore from a file. |
| `-o`, `--output FILE` | Write command output to a file instead of displaying it on the console. |

---

# `deps`

List the dependencies detected in the project.

By default, `deps` displays dependencies as a flat list.

## Options

| Option | Description |
| --- | --- |
| `--tree` | Display dependencies grouped by file as a file → dependency tree. |
| `--reverse` | Display the dependency → file tree. Requires `--tree`. |
| `--unused` | Display unused imports instead of the complete dependency list. |
| `-t`, `--type TYPES` | Filter dependencies by type. Accepted values are `stdlib`, `third-party`, `local`, or `all`. Multiple values can be supplied as a comma-separated list. |
| `-o`, `--output FILE` | Write the output to a JSON file. |

## Examples

List dependencies:

```bash
digdep deps ./myproject
```

Show only third-party dependencies:

```bash
digdep deps ./myproject --type third-party
```

Show standard library and local dependencies:

```bash
digdep deps ./myproject --type stdlib,local
```

Show the file → dependency tree:

```bash
digdep deps ./myproject --tree
```

Show the dependency → file tree:

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

Write dependencies to JSON:

```bash
digdep deps ./myproject -o dependencies.json
```

Write the file → dependency tree to JSON:

```bash
digdep deps ./myproject --tree -o file_tree.json
```

Write the dependency → file tree to JSON:

```bash
digdep deps ./myproject --tree --reverse -o dependency_tree.json
```

Write unused imports to JSON:

```bash
digdep deps ./myproject --unused -o unused.json
```

Write the unused imports tree to JSON:

```bash
digdep deps ./myproject --unused --tree -o unused_tree.json
```

Ignore directories while scanning:

```bash
digdep deps ./myproject --ignore venv __pycache__ tests
```

Read ignored paths from a file:

```bash
digdep deps ./myproject --ignore-file .digdepignore
```

Redirect console output using the shell:

```bash
digdep deps ./myproject --tree > dependencies.txt
```

---

# `find-dep`

Find files that import a specified dependency.

The dependency name is provided as a positional argument.

## Usage

```bash
digdep find-dep DEPENDENCY <path> [OPTIONS]
```

## Options

| Option | Description |
| --- | --- |
| `--tree` | Display matching files as a directory tree. |
| `-sl`, `--showlines` | Show the import lines where the dependency is found. Requires `--tree`. |
| `-o`, `--output FILE` | Write the output to a JSON file. |
| `-i`, `--ignore NAME [NAME ...]` | Ignore one or more directories or files. |
| `-I`, `--ignore-file FILE` | Read directories or files to ignore from a file. |

## Examples

Find files importing `requests`:

```bash
digdep find-dep requests ./myproject
```

Display matching files as a tree:

```bash
digdep find-dep requests ./myproject --tree
```

Display the import lines where the dependency is found:

```bash
digdep find-dep requests ./myproject --tree --showlines
```

Write matching files to JSON:

```bash
digdep find-dep requests ./myproject -o requests.json
```

Write the tree representation to JSON:

```bash
digdep find-dep requests ./myproject --tree -o requests.json
```

Include import lines in the tree JSON:

```bash
digdep find-dep requests ./myproject --tree --showlines -o requests.json
```

Ignore directories:

```bash
digdep find-dep requests ./myproject --ignore venv __pycache__ tests
```

Read ignored paths from a file:

```bash
digdep find-dep requests ./myproject --ignore-file .digdepignore
```

---

# `stats`

Display dependency statistics for the project.

## Options

| Option | Description |
| --- | --- |
| `-tn`, `--topn NUM` | Display the top **NUM** imported dependencies. Defaults to `5`. |

## Examples

Display project statistics:

```bash
digdep stats ./myproject
```

Display the top 10 imported dependencies:

```bash
digdep stats ./myproject --topn 10
```

---

# Command Examples

List dependencies:

```bash
digdep deps ./myproject
```

Show the file → dependency tree:

```bash
digdep deps ./myproject --tree
```

Show the dependency → file tree:

```bash
digdep deps ./myproject --tree --reverse
```

Find unused imports:

```bash
digdep deps ./myproject --unused
```

Find files importing a dependency:

```bash
digdep find-dep requests ./myproject
```

Find dependency usage and show import lines:

```bash
digdep find-dep requests ./myproject --tree --showlines
```

Export a result as JSON:

```bash
digdep deps ./myproject --tree -o dependencies.json
```

Ignore directories:

```bash
digdep deps ./myproject --ignore venv __pycache__ tests
```

Display dependency statistics:

```bash
digdep stats ./myproject --topn 10
```

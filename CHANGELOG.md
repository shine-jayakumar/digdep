# Changelog

All notable changes to this project will be documented in this file.
# Changelog

## [0.1.1] - 2026-08-08

### Added

- Added the `find-dep` command for finding files that import a specific dependency.
  - Added `--tree` output mode.
  - Added `--showlines` to display the exact import lines.
  - Added JSON output support.
- Added a CLI dispatcher architecture to separate command dispatching from argument parsing and analyzer execution.
- Added dedicated CLI option classes for translating command-line arguments into analyzer arguments.
- Added command handler classes for:
  - `deps`
  - `stats`
  - `find-dep`
- Added validation for incompatible CLI arguments, including:
  - `--reverse` requires `--tree`.
  - `--reverse` cannot be combined with `--unused`.
  - `--showlines` requires `--tree`.
- Added dedicated CLI exceptions for unmapped commands, invalid analyzer functions, and invalid arguments.
- Added support for dependency lookup through the analyzer API, including finding dependency instances and displaying/exporting files containing a dependency.
- Added support for displaying and exporting dependency file trees with optional import line information.

### Changed

- Consolidated the previous `file-tree`, `dep-tree`, and `unused-imports` CLI commands into the `deps` command using options:
  - `--tree`
  - `--reverse`
  - `--unused`
- Updated the CLI to use the new dispatcher and command-handler architecture.
- Refactored CLI dependency type filtering into a dedicated `DepFilter` option.
- Renamed and aligned dependency tree analyzer APIs around:
  - `filedep_tree`
  - `depfiles_tree`
- Updated imported-name tracking in the AST visitor from `imports` to `import_names`.
- Updated CLI and API documentation to reflect the new command structure and analyzer APIs.

### Documentation

- Updated CLI documentation for the consolidated `deps` command and new `find-dep` command.
- Updated API documentation with the new dependency lookup, tree, filtering, and unused-import APIs.
- Added examples for dependency filtering, dependency lookup, tree output, JSON export, and showing import lines.

### Tests

- Updated imported-name visitor tests to use the new `import_names` attribute.
- Updated visitor assertions to reflect the renamed import tracking structure.


## [0.0.9] - 2026-08-02

### Added
- Add the `--topn` (`-tn`) option to the `stats` command for displaying the top N dependencies.

### Changed
- Refactor dependency type counting.
- Update the statistics output to display a configurable number of top dependencies.


## [0.0.8] - 2026-08-01

### Added
- Add dependency statistics with file, import, and dependency metrics.
- Add the `stats` CLI command.
- Add the `Stats` API for programmatic access to analysis metrics.
- Add dedicated CLI and Python API documentation.
- Add tests for dependency statistics and analyzer functionality.

### Changed
- Rename `scan()` to `analyze()` in the Python API.
- Improve dependency analysis to collect project statistics.
- Update the README with a simplified quick start and links to dedicated documentation.

### Documentation
- Add comprehensive CLI documentation.
- Add comprehensive Python API documentation.


## [0.0.7] - 2026-08-01

### Added
- Add support for detecting unused imports.
- Add the `unused-imports` CLI command to display unused imports by file.

### Changed
- Enhance AST analysis to track imported symbols and their usage.
- Improve dependency analysis by recording import metadata and usage information.

### Documentation
- Document the `unused-imports` command in the README.


## [0.0.6] - 2026-07-29

### Added
- Detect and classify local dependencies imported using relative imports.
- Add support for returning JSON output as a string when no output file is specified.

### Changed
- Update dependency scanning to preserve import level information.
- Improve dependency classification by distinguishing standard library, third-party, and local modules.
- Enhance the dependency visitor to capture import levels for both `import` and `from ... import` statements.
- Add examples to the README demonstrating JSON export and filtered JSON output.

### Fixed
- Correctly identify local dependencies imported via relative imports.
- Handle module-less relative import statements (for example, `from . import module`) during dependency analysis.

### Documentation
- Update the README with JSON export examples.
- Rename the `packages` command to `deps`.
- Update the version badge to **0.0.6**.


## [0.0.5] - 2026-07-29

### Added
- Support exporting dependency lists as JSON.
- Support exporting file-dependency trees as JSON.
- Support exporting dependency-file trees as JSON.
- Add `-o` / `--output` CLI option to write command output to a file.

### Changed
- Rename the `packages` command to `deps`.
- Rename package-related APIs to use **dependency** instead of package. 
- Refactor CLI command handling to use a generic command dispatcher.
- Refactor dependency type parsing into a dedicated helper function.

### Fixed
- Improve CLI error handling by replacing abrupt exits with custom exceptions.
- Add centralized exception handling for command execution.

### Removed
- Remove the obsolete `analyzer_bak.py` backup file.


## [0.0.4] - 2026-07-28

### Added

- Add support for loading ignored directories from a text file using 
- the `--ignore-file` (`-I`) CLI option.
- Add `DepAnalyzer.ignore_from_file()` to populate the ignore list from a file.
- Add `DepAnalyzer.ignorelist` property to expose the current ignore list.

### Fixed

- Fix dependency type filtering in the CLI so the selected dependency types are applied correctly.

### Changed

- Bump package version to **0.0.4**.


## [0.0.3] - 2026-07-28

### Changed
- Export __version__ from digdep to allow digdep.__version__


## [0.0.2] - 2026-07-28

### Fixed
- Unterminated string in argparser


## [0.0.1] - Initial Release - 2026-07-28

### Added

- Initial release of DigDep.
- Recursive scanning of Python projects.
- Package listing (`packages` command).
- File → Dependency tree (`file-tree` command).
- Dependency → File tree (`dep-tree` command).
- Dependency filtering by type:
  - Standard library
  - Third-party
  - Local
  - Unknown
- Ignore files and directories during project scanning.
- CLI interface with built-in help and version information.
- Library API for integrating DigDep into Python applications.

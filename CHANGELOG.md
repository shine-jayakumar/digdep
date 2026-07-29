# Changelog

All notable changes to this project will be documented in this file.

---

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

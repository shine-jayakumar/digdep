# Changelog

All notable changes to this project will be documented in this file.

---

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

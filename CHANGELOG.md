# Changelog

All notable changes to this project will be documented in this file.

---

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
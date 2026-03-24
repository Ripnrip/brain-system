# Changelog

All notable changes to Brain-System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Native iOS app with Realm sync
- Cross-vault backlinks
- AI-powered note suggestions
- Full-text search with FTS5
- Plugin system for custom parsers

## [1.2.0] - 2024-01-15

### Added
- Graph visualization with cosmos.gl
- Web interface for cross-device access
- Interactive node details panel
- Vault filtering in graph view
- Search filter in graph visualization

### Changed
- Improved graph algorithm with better clustering
- Enhanced web UI with modern dark theme
- Better mobile responsive design

### Fixed
- Graph rendering issues with large datasets
- Memory leaks in graph data loading

## [1.1.0] - 2024-01-10

### Added
- Multi-vault task management
- Task priority levels (high, medium, low)
- Todoist integration support
- Task completion tracking
- `brain tasks --all` for cross-vault tasks

### Changed
- Improved database schema for tasks
- Better task sorting by priority and date

### Fixed
- Task duplication issues
- Priority sorting bugs

## [1.0.0] - 2024-01-05

### Added
- Initial release of multi-vault brain system
- SQLite indexing for fast search
- CLI with vault management
- Full-text search across vaults
- PARA folder detection
- YAML frontmatter parsing
- Auto-sync with LaunchAgent
- Wikilink extraction
- Tag indexing
- Cross-vault search

## [0.9.0] - 2023-12-20

### Added
- Beta release
- Single vault sync (sync.py)
- Basic search functionality
- Database schema design
- Markdown parsing
- Obsidian vault detection

---

## Version History Summary

| Version | Date | Key Features |
|---------|------|--------------|
| 1.2.0 | 2024-01-15 | Graph visualization, web interface |
| 1.1.0 | 2024-01-10 | Task management, Todoist sync |
| 1.0.0 | 2024-01-05 | Multi-vault system, CLI, auto-sync |
| 0.9.0 | 2023-12-20 | Beta: single vault sync, basic search |

---

## Breaking Changes

### 1.0.0
- Database schema changed from 0.9.0 - requires re-sync
- CLI command format changed (run `brain` without args for help)

### Migration Guide

If upgrading from 0.9.0 to 1.0.0:

```bash
# Backup old databases
cp -r ~/Library/Mobile\ Documents/iCloud~md~obsidian/*/brain ~/brain-backup

# Run sync to rebuild with new schema
brain sync
```

---

## Release Cadence

- **Major releases** (X.0.0): Quarterly - major features, breaking changes
- **Minor releases** (1.X.0): Monthly - new features, backward compatible
- **Patch releases** (1.0.X): As needed - bug fixes, no API changes

---

## Future Roadmap

See [README.md](README.md#roadmap) for planned features.

# Brain-System Documentation

Complete documentation for the Brain-System knowledge management platform.

## Quick Links

- [README](../README.md) - Project overview and quick start
- [Setup Guide](SETUP.md) - Installation and configuration
- [User Guide](USER_GUIDE.md) - Daily usage and workflows
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions
- [Configuration](CONFIGURATION.md) - Customization options
- [iOS Shortcuts](IOS_SHORTCUTS.md) - Mobile access guide
- [Roadmap](ROADMAP.md) - Planned features

## API Reference

- [API Documentation](../API.md) - Complete API reference
- [Architecture](../ARCHITECTURE.md) - System design and data flow

## Contributing

- [Contributing Guide](../CONTRIBUTING.md) - How to contribute
- [Changelog](../CHANGELOG.md) - Version history

## Documentation Overview

### For Users

1. **[Setup Guide](SETUP.md)** - Get Brain-System running on your Mac
2. **[User Guide](USER_GUIDE.md)** - Learn daily workflows and features
3. **[iOS Shortcuts](IOS_SHORTCUTS.md)** - Access from your iPhone

### For Developers

1. **[API Documentation](../API.md)** - CLI and web API reference
2. **[Architecture](../ARCHITECTURE.md)** - System design and internals
3. **[Contributing Guide](../CONTRIBUTING.md)** - Contribution guidelines

### For Administrators

1. **[Configuration](CONFIGURATION.md)** - Customization and advanced setup
2. **[Troubleshooting](TROUBLESHOOTING.md)** - Debug and resolve issues
3. **[Roadmap](ROADMAP.md)** - Future development plans

## Key Concepts

### Vaults

Brain-System manages multiple Obsidian vaults:

- **realm** - Main second brain (PARA, Zettelkasten)
- **remote** - Cloud-synced vault (Todoist integration)
- **apple** - Apple Notes exported to Obsidian
- **assets** - Attachments and media
- **second** - Local development vault

### Core Features

- **Fast Search** - SQLite-powered full-text search (<10ms)
- **Graph Visualization** - Interactive knowledge graph
- **Task Management** - Track and query tasks across vaults
- **Auto-Sync** - LaunchAgent keeps databases updated
- **Web Interface** - Access from any device

## Quick Reference

### CLI Commands

```bash
brain vaults              # List all vaults
brain search "query"      # Search current vault
brain search "q" --all    # Search all vaults
brain tasks               # Show pending tasks
brain tasks --all         # Tasks across all vaults
brain add-task "task"     # Add new task
brain sync                # Re-index all vaults
brain stats               # Show statistics
```

### Web Interface

```bash
python3 web.py
# Visit: http://localhost:5789
```

### Database Locations

Each vault stores its database in `<vault>/brain/brain.db`:

```bash
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/
├── Realm-Obsidian/brain/brain.db
├── Remote-Vault/brain/brain.db
├── Apple Notes/brain/brain.db
└── ...
```

## Getting Help

1. Check [Troubleshooting](TROUBLESHOOTING.md) for common issues
2. Review [Configuration](CONFIGURATION.md) for customization
3. Open an issue on GitHub for bugs
4. Start a discussion for questions

## Documentation Structure

```
Brain-System/
├── README.md              # Project overview
├── ARCHITECTURE.md        # System design
├── API.md                 # API reference
├── CHANGELOG.md           # Version history
├── CONTRIBUTING.md        # Contribution guide
└── docs/
    ├── INDEX.md           # This file
    ├── SETUP.md           # Installation guide
    ├── USER_GUIDE.md      # User documentation
    ├── TROUBLESHOOTING.md # Troubleshooting
    ├── CONFIGURATION.md   # Configuration
    ├── IOS_SHORTCUTS.md   # Mobile access
    └── ROADMAP.md         # Future plans
```

## Version

Current version: **1.2.0**

Documentation last updated: 2024-01-15

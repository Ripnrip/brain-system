# Brain-System

A distributed second brain system that manages multiple Obsidian vaults with fast SQLite indexing, full-text search, task management, and interactive graph visualization.

## Overview

Brain-System provides instant search and visualization across your Obsidian vaults by indexing all markdown notes into local SQLite databases. It supports:

- **Multi-vault management** - Index and search across 5+ vaults simultaneously
- **Full-text search** - Find any note in milliseconds across all vaults
- **Task management** - Track and query tasks from any vault
- **Graph visualization** - Interactive knowledge graph with cosmos.gl
- **Web interface** - Access from any device on your network
- **Auto-sync** - LaunchAgent keeps databases updated every 5 minutes

## Quick Start

### Installation

```bash
# Clone to your Obsidian vaults directory
cd ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Brain-System

# Install dependencies (Python 3.11+)
pip3 install flask

# Make CLI executable
chmod +x brain
mkdir -p ~/.brain
cp multi-brain.py ~/.brain/
cp brain ~/.brain/

# Add to PATH (add to ~/.zshrc)
export PATH="$HOME/.brain:$PATH"
```

### First Run

```bash
# Sync all vaults (builds databases)
brain sync

# List all vaults with stats
brain vaults

# Search across all vaults
brain search "python" --all

# Start web server
python3 web.py
```

## Commands

### CLI Commands

```bash
# Vault management
brain vaults              # List all vaults with note counts
brain sync                # Import all markdown files into databases

# Search
brain search <query>      # Search current vault
brain search <query> --all # Search all vaults

# Tasks
brain tasks               # Show pending tasks in current vault
brain tasks --all         # Show tasks across all vaults
brain add-task "Buy milk" # Add task to current vault
brain add-task "Call mom" realm # Add to specific vault

# Statistics
brain stats               # Show statistics for all vaults

# Navigation
brain cd <vault>          # Change to vault directory
brain open <vault>        # Open vault in Obsidian
```

### Web Server

```bash
# Start web interface
python3 web.py

# Access at:
# http://localhost:5789          # Search interface
# http://localhost:5789/graph-view # Graph visualization
```

## Architecture

Brain-System consists of four main components:

1. **multi-brain.py** - Core CLI for multi-vault management
2. **sync.py** - Standalone vault sync script
3. **web.py** - Flask web server with search and graph API
4. **graph.html** - Interactive graph visualization

## Vaults

| Vault | Purpose | Path |
|-------|---------|------|
| **realm** | Main second brain (PARA, Zettelkasten) | `iCloud~/Realm-Obsidian` |
| **remote** | Cloud-synced with Todoist integration | `iCloud~/Remote-Vault` |
| **apple** | Apple Notes exported to Obsidian | `iCloud~/Apple Notes` |
| **assets** | Attachments and media | `iCloud~/Apple Notes Assets` |
| **second** | Local development/backup | `~/Documents/SecondBrain` |

## Performance

- **Search speed**: <10ms for 1,400+ notes
- **Index sync**: ~2 seconds per vault
- **Database size**: ~5MB per 1,000 notes
- **Memory usage**: ~50MB for web server

## Requirements

- Python 3.11+
- macOS (for LaunchAgent auto-sync)
- Obsidian (optional, for viewing notes)
- Flask (for web interface)

## Troubleshooting

### Search not finding notes

```bash
# Re-sync all vaults
brain sync
```

### Database errors

```bash
# Delete and recreate database
rm ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Realm-Obsidian/brain/brain.db
brain sync
```

### Auto-sync not working

```bash
# Check LaunchAgent status
launchctl list | grep brain

# View sync logs
tail -f /tmp/brain-sync.log

# Restart LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.brain.sync.plist
launchctl load ~/Library/LaunchAgents/com.brain.sync.plist
```

### Web server won't start

```bash
# Check port availability
lsof -i :5789

# Kill existing process
kill -9 $(lsof -ti :5789)
```

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design and data flow
- [API.md](API.md) - Complete API reference
- [CHANGELOG.md](CHANGELOG.md) - Version history
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [docs/](docs/) - Detailed guides and tutorials

## License

MIT

## Author

Created for personal knowledge management with Obsidian.

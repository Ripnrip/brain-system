# 🧠 Multi-Vault Brain System

## Overview

Your second brain is now a distributed system across 5 vaults, each optimized for specific purposes. All vaults are indexed in local SQLite databases for instant search.

## Vaults

| Vault | Notes | Purpose | Path |
|-------|-------|---------|------|
| **realm** | 692 | Main second brain (PARA, Zettelkasten) | iCloud/Realm-Obsidian |
| **apple** | 662 | Apple Notes archive | iCloud/Apple Notes |
| **second** | 37 | Local development/backup | ~/Documents/SecondBrain |
| **remote** | 29 | Todoist integration, mobile | iCloud/Remote-Vault |
| **assets** | 2 | Attachments, media | iCloud/Apple Notes Assets |

**Total: 1,422 notes** across all vaults

## Installation

The brain CLI is installed at `~/.brain/brain`.

Add to PATH (already done):
```bash
export PATH="$HOME/.brain:$PATH"
```

## Commands

```bash
# List all vaults
brain vaults

# Search current vault
brain search "python"

# Search all vaults
brain search "python" --all

# Show tasks
brain tasks

# Show tasks across all vaults
brain tasks --all

# Add a task
brain add-task "Call mom Sunday"

# Add to specific vault
brain add-task "Project idea" realm

# Sync all vaults
brain sync

# Statistics
brain stats

# Open vault in Obsidian
brain open realm
```

## Performance

| Operation | Speed |
|-----------|-------|
| Search 1,422 notes | ~10ms |
| Get note by ID | ~1ms |
| List all tasks | ~5ms |
| Full-text query | Instant |

## Auto-Sync

The brain system auto-syncs every 5 minutes via LaunchAgent.

Check sync status:
```bash
tail -f /tmp/brain-sync.log
```

Manual sync:
```bash
brain sync
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Brain CLI (~/.brain/)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  realm   │  │  remote  │  │  apple   │  │  assets  │    │
│  │  692     │  │   29     │  │  662     │  │    2     │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓ brain sync
                    ┌───────────────┐
                    │ Markdown Files│
                    │   (iCloud)    │
                    └───────────────┘
                            │
                            ↓
                    All your devices
```

## Vault-Specific Documentation

Each vault has a `BRAIN.md` file with detailed information:

- [Realm-Obsidian/BRAIN.md](~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Realm-Obsidian/BRAIN.md)
- [Remote-Vault/BRAIN.md](~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Remote-Vault/BRAIN.md)
- [Apple Notes/BRAIN.md](~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Apple Notes/BRAIN.md)

## Database Schema

Each vault has a SQLite database with:

```sql
notes:
  - id, title, content, tags
  - created_at, updated_at
  - para_folder (Inbox, Projects, etc.)
  - vault (realm, remote, apple, etc.)

tasks:
  - id, content, completed
  - priority, due_date
  - vault, note_id
```

## Troubleshooting

### Search not working
```bash
brain sync  # Re-index all vaults
```

### Vault not found
```bash
brain vaults  # List available vaults
```

### Database error
```bash
# Delete and recreate specific vault
rm ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Realm-Obsidian/brain/brain.db
brain sync
```

## LaunchAgent

Auto-sync runs every 5 minutes:

```bash
# Check status
launchctl list | grep brain

# View logs
tail -f /tmp/brain-sync.log

# Restart
launchctl unload ~/Library/LaunchAgents/com.brain.sync.plist
launchctl load ~/Library/LaunchAgents/com.brain.sync.plist
```

## Future

- [ ] Native iOS app with Realm sync
- [ ] Graph visualization across vaults
- [ ] AI-powered note suggestions
- [ ] Cross-vault backlinks
- [ ] Web interface for search

---

**Total indexed: 1,422 notes | Auto-sync: Every 5 minutes | Search speed: <10ms**

# User Guide

Learn how to use Brain-System effectively for knowledge management.

## Table of Contents

- [Basic Concepts](#basic-concepts)
- [Daily Workflow](#daily-workflow)
- [Searching](#searching)
- [Task Management](#task-management)
- [Graph Visualization](#graph-visualization)
- [Advanced Usage](#advanced-usage)

## Basic Concepts

### What is Brain-System?

Brain-System indexes your Obsidian vaults into SQLite databases for instant search and visualization. Think of it as a "search engine for your brain."

### Key Concepts

- **Vaults** - Individual Obsidian vaults (realm, remote, apple, etc.)
- **Notes** - Individual markdown files
- **Links** - Connections between notes (wikilinks)
- **Tasks** - Action items from notes
- **PARA** - Organizational system (Projects, Areas, Resources, Archives)

### The Brain-System Directory Structure

```
Brain-System/
├── brain              # CLI executable
├── multi-brain.py     # Core multi-vault logic
├── sync.py            # Vault sync script
├── web.py             # Web server
├── graph.html         # Graph visualization
└── docs/              # Documentation
```

## Daily Workflow

### 1. Morning Review

```bash
# Check pending tasks across all vaults
brain tasks --all

# Quick scan of recent notes
brain search "" --all | head -20
```

### 2. During Work

```bash
# Find relevant notes
brain search "project name" --all

# Add quick tasks
brain add-task "Follow up with client"

# Check specific vault
brain search "meeting" realm
```

### 3. Evening Review

```bash
# Review completed tasks
brain sync

# Check statistics
brain stats
```

## Searching

### Basic Search

```bash
brain search "query"
```

Searches note titles and content in the current vault.

### Cross-Vault Search

```bash
brain search "query" --all
```

Searches across all vaults.

### Search Tips

1. **Use specific terms** - Unique words work better than common ones
2. **Search by tag** - Include the tag prefix
   ```bash
   brain search "#important"
   ```
3. **Search by folder** - Use PARA folder names
   ```bash
   brain search "Projects"
   ```

### Web Search

Access `http://localhost:5789` for a visual search interface.

Features:
- Real-time search as you type
- Vault filtering
- Note preview
- Tag display
- Mobile-friendly

## Task Management

### View Tasks

```bash
# Current vault
brain tasks

# All vaults
brain tasks --all
```

### Add Tasks

```bash
# To current vault
brain add-task "Buy milk"

# To specific vault
brain add-task "Project deadline" realm
```

### Task Priorities

Tasks have priority levels:
- **1** - High priority
- **2** - Medium priority (default)
- **3** - Low priority

### Task Workflow

1. Capture tasks in notes using `- [ ]` format
2. Sync with `brain sync`
3. View with `brain tasks`
4. Complete in Obsidian with `- [x]`
5. Re-sync to update status

## Graph Visualization

### Access the Graph

```bash
# Start web server
python3 web.py

# Visit in browser
open http://localhost:5789/graph-view
```

### Graph Features

- **Node size** - Indicates number of connections
- **Node color** - Indicates vault
- **Line color** - Indicates connection type
- **Interactivity** - Drag nodes, click for details

### Connection Types

| Type | Description | Color |
|------|-------------|-------|
| Wikilink | Direct `[[link]]` | Purple |
| Similar | Shared content | Green |
| Tag | Common tags | Orange |
| Folder | Same PARA folder | Pink |

### Using the Graph

1. **Explore clusters** - Groups of related notes
2. **Find bridges** - Notes connecting different topics
3. **Identify orphans** - Notes with few connections
4. **Discover relationships** - See how topics relate

## Advanced Usage

### PARA Organization

Brain-System automatically detects PARA folders:

```bash
# Find all Projects
brain search "Projects"

# View Areas
brain search "Areas"
```

### Wikilink Best Practices

1. **Use descriptive links** - `[[Machine Learning Basics]]` not `[[ML]]`
2. **Link liberally** - Connect related concepts
3. **Create index notes** - Hub pages for topics
4. **Use aliases** - `[[Note Title|Alias]]` for variations

### Tag Strategy

1. **Use consistent tags** - Establish a system
2. **Tag by context** - `#work`, `#personal`, `#ideas`
3. **Tag by status** - `#todo`, `#in-progress`, `#done`
4. **Avoid over-tagging** - 3-5 tags per note

### Advanced Queries

```bash
# Find notes with specific tags
brain search "#python AND #tutorial"

# Find recent notes in a folder
brain search "Projects" | grep "2024"

# Count notes by vault
brain stats
```

### Aliases and Shell Functions

Add to `~/.zshrc`:

```bash
# Quick search alias
alias bs='brain search'

# Quick tasks alias
alias bt='brain tasks --all'

# Quick add function
ba() {
    brain add-task "$*"
}

# Open in Obsidian
bo() {
    brain open "${1:-realm}"
}
```

### Integration with Obsidian

1. **Command Palette** - Create Obsidian commands that run brain CLI
2. **Hotkeys** - Bind hotkeys to brain commands
3. **Dataview** - Combine brain search with Dataview queries
4. **Templates** - Include brain results in templates

## Tips and Tricks

### 1. Daily Note Workflow

```bash
# Create daily note with today's tasks
brain tasks --all >> $(date +%Y-%m-%d).md
```

### 2. Weekly Review

```bash
# Get weekly summary
brain stats
brain tasks --all
brain search "review" --all
```

### 3. Project Dashboard

Create a project note with embedded queries:

```markdown
# Project Alpha

## Tasks
<!-- Run: brain tasks --all | grep "Alpha" -->

## Related Notes
<!-- Run: brain search "Alpha" --all -->
```

### 4. Quick Capture

```bash
# Quick note function
qc() {
    echo "# $(date +%H:%M) $*" >> ~/quick-capture.md
    brain sync
}
```

### 5. Search Operators

Combine searches:

```bash
# Find notes with multiple terms
brain search "python" | brain search "tutorial"

# Exclude terms (using grep)
brain search "python" | grep -v "basic"
```

## Best Practices

1. **Sync regularly** - Use LaunchAgent for automatic sync
2. **Use descriptive titles** - Makes search more effective
3. **Link related notes** - Builds knowledge graph
4. **Tag consistently** - Enables filtering
5. **Review the graph** - Discover connections
6. **Clean up orphan notes** - Link or delete them
7. **Back up databases** - Keep copies of `brain/` folders

## Keyboard Shortcuts (Web)

| Key | Action |
|-----|--------|
| `/` | Focus search |
| `Escape` | Close modal |
| `Tab` | Next result |

## Troubleshooting

### Search returns no results

```bash
# Re-sync vaults
brain sync

# Check vault exists
brain vaults
```

### Graph won't load

```bash
# Reduce data size
# Edit web.py: limit points to 500

# Clear browser cache
# Or use incognito mode
```

### Tasks not showing

```bash
# Check note format
# Tasks must use - [ ] format

# Re-sync
brain sync
```

## Next Steps

- Set up [mobile access](IOS_SHORTCUTS.md)
- Customize [configuration](CONFIGURATION.md)
- Explore [API](../API.md) for automation
